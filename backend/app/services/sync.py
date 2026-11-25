import logging
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import decrypt_token
from app.models.ai import SyncState
from app.models.email import EmailAccount, EmailMessage, EmailThread
from app.services.gmail import build_gmail_service, parse_gmail_message

logger = logging.getLogger(__name__)


async def sync_account_emails(account_id_str: str, max_messages: int = 50) -> int:
    """
    Fetch recent emails from Gmail for given account and persist them to DB.
    Returns count of processed messages.
    """
    account_uuid = uuid.UUID(account_id_str)

    async with AsyncSessionLocal() as db:
        # Load account
        query = select(EmailAccount).where(EmailAccount.id == account_uuid)
        result = await db.execute(query)
        account = result.scalar_one_or_none()

        if not account or not account.is_active:
            logger.warning(f"EmailAccount {account_id_str} not found or inactive.")
            return 0

        # Load or create sync state
        state_query = select(SyncState).where(SyncState.account_id == account.id)
        state_res = await db.execute(state_query)
        sync_state = state_res.scalar_one_or_none()
        if not sync_state:
            sync_state = SyncState(
                account_id=account.id,
                user_id=account.user_id,
                sync_status="syncing",
            )
            db.add(sync_state)
        else:
            sync_state.sync_status = "syncing"
            sync_state.error_message = None

        await db.commit()

        try:
            access_token = decrypt_token(account.access_token_encrypted or "")
            refresh_token = (
                decrypt_token(account.refresh_token_encrypted)
                if account.refresh_token_encrypted
                else None
            )

            service = build_gmail_service(access_token, refresh_token)

            # List recent messages from Gmail inbox
            response = service.users().messages().list(userId="me", maxResults=max_messages).execute()
            messages_meta = response.get("messages", [])

            processed_count = 0

            for m_meta in messages_meta:
                m_id = m_meta["id"]

                # Check if message already stored
                existing_msg_query = select(EmailMessage).where(
                    EmailMessage.provider_message_id == m_id
                )
                existing_res = await db.execute(existing_msg_query)
                if existing_res.scalar_one_or_none():
                    continue

                # Fetch full message
                raw_msg = (
                    service.users()
                    .messages()
                    .get(userId="me", id=m_id, format="full")
                    .execute()
                )
                parsed = parse_gmail_message(raw_msg)

                # Find or create EmailThread
                thread_query = select(EmailThread).where(
                    EmailThread.account_id == account.id,
                    EmailThread.provider_thread_id == parsed["provider_thread_id"],
                )
                thread_res = await db.execute(thread_query)
                thread = thread_res.scalar_one_or_none()

                if not thread:
                    thread = EmailThread(
                        account_id=account.id,
                        user_id=account.user_id,
                        provider_thread_id=parsed["provider_thread_id"],
                        subject=parsed["subject"],
                        snippet=parsed["snippet"],
                        is_read=parsed["is_read"],
                        last_message_at=parsed["timestamp"],
                    )
                    db.add(thread)
                    await db.flush()
                else:
                    thread.snippet = parsed["snippet"]
                    if parsed["timestamp"] and (
                        not thread.last_message_at
                        or parsed["timestamp"] > thread.last_message_at
                    ):
                        thread.last_message_at = parsed["timestamp"]

                # Create EmailMessage
                new_msg = EmailMessage(
                    thread_id=thread.id,
                    account_id=account.id,
                    user_id=account.user_id,
                    provider_message_id=parsed["provider_message_id"],
                    sender_email=parsed["sender_email"],
                    sender_name=parsed["sender_name"],
                    recipient_emails=parsed["recipient_emails"],
                    subject=parsed["subject"],
                    body_text=parsed["body_text"],
                    body_html=parsed["body_html"],
                    timestamp=parsed["timestamp"],
                    is_read=parsed["is_read"],
                    labels=parsed["labels"],
                )
                db.add(new_msg)
                processed_count += 1

            sync_state.sync_status = "idle"
            sync_state.last_sync_at = datetime.now(timezone.utc)
            await db.commit()
            return processed_count

        except Exception as exc:
            logger.error(f"Sync error for account {account_id_str}: {exc}", exc_info=True)
            sync_state.sync_status = "error"
            sync_state.error_message = str(exc)
            await db.commit()
            raise
