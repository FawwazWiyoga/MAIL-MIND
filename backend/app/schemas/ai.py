from datetime import datetime
from typing import Literal
import uuid
from pydantic import BaseModel, Field


class ExtractedActionItem(BaseModel):
    description: str = Field(..., description="Actionable task or follow-up requested in the email")
    due_date: str | None = Field(None, description="ISO date or mentioned deadline if specified in email, otherwise null")
    priority: Literal["critical", "high", "medium", "low"] = "medium"


class EmailAnalysisResult(BaseModel):
    summary: str = Field(..., description="A clear, 2-3 sentence summary of the email content and purpose")
    key_points: list[str] = Field(default_factory=list, description="Key facts, decisions, or dates mentioned")
    category: Literal[
        "Work",
        "Personal",
        "Academic",
        "Finance",
        "Promotion",
        "Notification",
        "Meeting",
        "Important",
        "Other",
    ] = Field(..., description="Classification category for the email")
    priority: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Priority level based on urgency, importance, and deadlines"
    )
    confidence_score: float = Field(default=0.9, ge=0.0, le=1.0)
    action_items: list[ExtractedActionItem] = Field(
        default_factory=list, description="List of tasks, requests, or deadlines requiring user action"
    )


class ReplyDraftRequest(BaseModel):
    email_id: uuid.UUID
    tone: Literal["professional", "formal", "friendly", "concise"] = "professional"
    instructions: str | None = None


class ReplyDraftResponse(BaseModel):
    draft: str
    tone: str


class ThreadSummaryResponse(BaseModel):
    thread_id: uuid.UUID
    summary: str
    message_count: int


class ActionItemCreate(BaseModel):
    description: str
    due_date: datetime | None = None
    priority: Literal["critical", "high", "medium", "low"] = "medium"
    message_id: uuid.UUID | None = None


class ActionItemUpdate(BaseModel):
    description: str | None = None
    due_date: datetime | None = None
    status: Literal["pending", "in_progress", "completed", "cancelled"] | None = None
    priority: Literal["critical", "high", "medium", "low"] | None = None


class ActionItemResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    message_id: uuid.UUID | None
    description: str
    due_date: datetime | None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
