import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import encrypt_token
from app.models.email import EmailAccount
from app.models.ai import SyncState
from app.models.user import User
from app.schemas.email import EmailAccountResponse
from app.services.google_auth import exchange_google_code, get_google_auth_url
from app.workers.tasks import sync_email_account

router = APIRouter()


@router.get("", response_model=list[EmailAccountResponse])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all connected email accounts for the current user."""
    query = select(EmailAccount).where(EmailAccount.user_id == current_user.id)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("/gmail/connect")
async def connect_gmail(current_user: User = Depends(get_current_user)):
    """Generate and return Google OAuth authorization URL."""
    auth_url = get_google_auth_url(user_id=str(current_user.id))
    return {"auth_url": auth_url}


@router.get("/gmail/callback")
async def gmail_callback(
    code: str = Query(...),
    state: str = Query(...),  # holds user_id
    db: AsyncSession = Depends(get_db),
):
    """
    Handle Google OAuth callback, save encrypted tokens, and schedule initial sync.
    """
    try:
        user_uuid = uuid.UUID(state)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    # Verify user exists
    user_query = select(User).where(User.id == user_uuid)
    user_res = await db.execute(user_query)
    user = user_res.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        google_tokens = await exchange_google_code(code)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"OAuth exchange failed: {str(exc)}")

    email_address = google_tokens["email_address"]
    access_token_enc = encrypt_token(google_tokens["access_token"])
    refresh_token_enc = (
        encrypt_token(google_tokens["refresh_token"])
        if google_tokens["refresh_token"]
        else None
    )

    # Check if account already exists
    acc_query = select(EmailAccount).where(
        EmailAccount.user_id == user.id,
        EmailAccount.email_address == email_address,
        EmailAccount.provider == "gmail",
    )
    acc_res = await db.execute(acc_query)
    account = acc_res.scalar_one_or_none()

    if account:
        account.access_token_encrypted = access_token_enc
        if refresh_token_enc:
            account.refresh_token_encrypted = refresh_token_enc
        account.token_expiry = google_tokens["token_expiry"]
        account.is_active = True
    else:
        account = EmailAccount(
            user_id=user.id,
            provider="gmail",
            email_address=email_address,
            access_token_encrypted=access_token_enc,
            refresh_token_encrypted=refresh_token_enc,
            token_expiry=google_tokens["token_expiry"],
            is_active=True,
        )
        db.add(account)
        await db.flush()

        # Initialize sync state
        sync_state = SyncState(
            account_id=account.id,
            user_id=user.id,
            sync_status="pending",
        )
        db.add(sync_state)

    await db.commit()
    await db.refresh(account)

    # Trigger Celery background sync task
    try:
        sync_email_account.delay(str(account.id))
    except Exception:
        # If celery broker is offline during dev, continue gracefully
        pass

    # Redirect user back to frontend dashboard settings
    return RedirectResponse(url="http://localhost:3000/settings?account_connected=true")


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_account(
    account_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Disconnect and delete an email account and associated data."""
    query = select(EmailAccount).where(
        EmailAccount.id == account_id,
        EmailAccount.user_id == current_user.id,
    )
    result = await db.execute(query)
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Email account not found")

    await db.delete(account)
    await db.commit()
