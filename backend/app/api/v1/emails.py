import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.email import EmailAccount, EmailMessage, EmailThread
from app.models.user import User
from app.schemas.email import EmailMessageResponse, EmailThreadResponse
from app.workers.tasks import sync_email_account

router = APIRouter()


@router.get("", response_model=list[EmailMessageResponse])
async def list_emails(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    account_id: uuid.UUID | None = Query(None),
    is_read: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List paginated emails for the authenticated user with optional filters."""
    query = select(EmailMessage).where(EmailMessage.user_id == current_user.id)

    if account_id:
        query = query.where(EmailMessage.account_id == account_id)
    if is_read is not None:
        query = query.where(EmailMessage.is_read == is_read)

    query = query.order_by(EmailMessage.timestamp.desc().nullslast())
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/search", response_model=list[EmailMessageResponse])
async def search_emails(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Keyword search across subject, sender, and email body."""
    search_pattern = f"%{q}%"
    query = (
        select(EmailMessage)
        .where(
            EmailMessage.user_id == current_user.id,
            or_(
                EmailMessage.subject.ilike(search_pattern),
                EmailMessage.sender_name.ilike(search_pattern),
                EmailMessage.sender_email.ilike(search_pattern),
                EmailMessage.body_text.ilike(search_pattern),
            ),
        )
        .order_by(EmailMessage.timestamp.desc().nullslast())
        .limit(limit)
    )

    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/{email_id}", response_model=EmailMessageResponse)
async def get_email(
    email_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get full details of a specific email message."""
    query = select(EmailMessage).where(
        EmailMessage.id == email_id,
        EmailMessage.user_id == current_user.id,
    )
    result = await db.execute(query)
    message = result.scalar_one_or_none()

    if message is None:
        raise HTTPException(status_code=404, detail="Email message not found")

    return message


@router.get("/{email_id}/thread", response_model=EmailThreadResponse)
async def get_email_thread(
    email_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get thread info associated with an email message."""
    msg_query = select(EmailMessage).where(
        EmailMessage.id == email_id,
        EmailMessage.user_id == current_user.id,
    )
    msg_res = await db.execute(msg_query)
    message = msg_res.scalar_one_or_none()

    if message is None:
        raise HTTPException(status_code=404, detail="Email message not found")

    thread_query = select(EmailThread).where(
        EmailThread.id == message.thread_id,
        EmailThread.user_id == current_user.id,
    )
    thread_res = await db.execute(thread_query)
    thread = thread_res.scalar_one_or_none()

    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")

    return thread


@router.post("/sync")
async def sync_emails(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger background email synchronization across all active accounts."""
    query = select(EmailAccount).where(
        EmailAccount.user_id == current_user.id,
        EmailAccount.is_active == True,
    )
    result = await db.execute(query)
    accounts = list(result.scalars().all())

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No connected email accounts found. Please connect your Gmail account in Settings.",
        )

    for acc in accounts:
        try:
            sync_email_account.delay(str(acc.id))
        except Exception:
            # If celery broker is not running locally during development, run inline
            from app.services.sync import sync_account_emails
            import asyncio
            asyncio.create_task(sync_account_emails(str(acc.id)))

    return {"message": f"Sync initiated for {len(accounts)} account(s)"}
