import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.ai import ActionItem
from app.models.user import User
from app.schemas.ai import ActionItemCreate, ActionItemResponse, ActionItemUpdate

router = APIRouter()


@router.get("", response_model=list[ActionItemResponse])
async def list_action_items(
    status_filter: str | None = Query(None, alias="status"),
    priority_filter: str | None = Query(None, alias="priority"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List action items extracted from emails with optional status and priority filtering."""
    query = select(ActionItem).where(ActionItem.user_id == current_user.id)

    if status_filter:
        query = query.where(ActionItem.status == status_filter)
    if priority_filter:
        query = query.where(ActionItem.priority == priority_filter)

    query = query.order_by(ActionItem.due_date.asc().nullslast(), ActionItem.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_action_item(
    payload: ActionItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a manual action item."""
    new_action = ActionItem(
        user_id=current_user.id,
        message_id=payload.message_id,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
        status="pending",
    )
    db.add(new_action)
    await db.commit()
    await db.refresh(new_action)
    return new_action


@router.patch("/{action_id}", response_model=ActionItemResponse)
async def update_action_item(
    action_id: uuid.UUID,
    payload: ActionItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update action item status (e.g., mark completed), priority, description, or due date."""
    query = select(ActionItem).where(
        ActionItem.id == action_id,
        ActionItem.user_id == current_user.id,
    )
    result = await db.execute(query)
    action = result.scalar_one_or_none()

    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    if payload.description is not None:
        action.description = payload.description
    if payload.due_date is not None:
        action.due_date = payload.due_date
    if payload.status is not None:
        action.status = payload.status
    if payload.priority is not None:
        action.priority = payload.priority

    action.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(action)
    return action


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action_item(
    action_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an action item."""
    query = select(ActionItem).where(
        ActionItem.id == action_id,
        ActionItem.user_id == current_user.id,
    )
    result = await db.execute(query)
    action = result.scalar_one_or_none()

    if action is None:
        raise HTTPException(status_code=404, detail="Action item not found")

    await db.delete(action)
    await db.commit()
