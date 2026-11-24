import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel


class EmailAccountResponse(BaseModel):
    id: uuid.UUID
    provider: str
    email_address: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class EmailMessageResponse(BaseModel):
    id: uuid.UUID
    thread_id: uuid.UUID
    sender_email: str | None
    sender_name: str | None
    subject: str | None
    body_text: str | None
    timestamp: datetime | None
    is_read: bool
    labels: list[Any]

    model_config = {"from_attributes": True}


class EmailThreadResponse(BaseModel):
    id: uuid.UUID
    subject: str | None
    snippet: str | None
    is_read: bool
    last_message_at: datetime | None

    model_config = {"from_attributes": True}
