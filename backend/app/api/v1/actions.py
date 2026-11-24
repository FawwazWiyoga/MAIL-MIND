from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()


@router.get("")
async def list_actions(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("", status_code=201)
async def create_action(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{action_id}")
async def update_action(action_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{action_id}", status_code=204)
async def delete_action(action_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Not implemented yet")
