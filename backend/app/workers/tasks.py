import asyncio
import logging
import uuid
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.email import EmailMessage
from app.services.ai.pipeline import analyze_email
from app.services.sync import sync_account_emails
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def sync_email_account(self, account_id: str):
    """Sync emails for a given account via Celery worker."""
    try:
        count = asyncio.run(sync_account_emails(account_id))
        logger.info(f"Successfully synced {count} emails for account {account_id}")
        return {"status": "ok", "messages_synced": count}
    except Exception as exc:
        logger.error(f"Failed to sync account {account_id}: {exc}")
        raise self.retry(exc=exc)


async def _process_email_ai_async(message_id_str: str):
    msg_uuid = uuid.UUID(message_id_str)
    async with AsyncSessionLocal() as db:
        query = select(EmailMessage).where(EmailMessage.id == msg_uuid)
        res = await db.execute(query)
        message = res.scalar_one_or_none()
        if not message:
            logger.warning(f"EmailMessage {message_id_str} not found for AI processing")
            return
        await analyze_email(message, db)
        logger.info(f"AI analysis completed for message {message_id_str}")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def process_email_ai(self, message_id: str):
    """Run AI processing (summarize, classify, prioritize, actions) on an email."""
    try:
        asyncio.run(_process_email_ai_async(message_id))
        return {"status": "ok", "message_id": message_id}
    except Exception as exc:
        logger.error(f"Failed AI processing for message {message_id}: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def generate_embedding(self, message_id: str):
    """Generate and store embedding for semantic search."""
    try:
        # Placeholder for Phase 4
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2)
def generate_daily_digest(self, user_id: str):
    """Generate daily digest for a specific user."""
    try:
        # Placeholder for Daily Digest
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def generate_daily_digest_all():
    """Triggered by beat — dispatches per-user digest tasks."""
    pass
