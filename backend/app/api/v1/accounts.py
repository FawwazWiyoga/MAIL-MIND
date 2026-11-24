from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email import EmailAccountResponse

router = APIRouter()


@router.get("", response_model=list[EmailAccountResponse])
async def list_accounts(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/gmail/connect")
async def connect_gmail():
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/gmail/callback")
async def gmail_callback(code: str, state: str | None = None):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{account_id}")
async def disconnect_account(account_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")
