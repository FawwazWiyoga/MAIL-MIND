from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.email import EmailMessageResponse, EmailThreadResponse

router = APIRouter()


@router.get("", response_model=list[EmailMessageResponse])
async def list_emails(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/search")
async def search_emails(q: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{email_id}", response_model=EmailMessageResponse)
async def get_email(email_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{email_id}/thread", response_model=EmailThreadResponse)
async def get_email_thread(email_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/sync")
async def sync_emails(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")
