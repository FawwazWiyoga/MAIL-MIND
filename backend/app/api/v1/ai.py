import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.ai import AIAnalysis, AIUsageLog
from app.models.email import EmailMessage, EmailThread
from app.models.user import User
from app.schemas.ai import ReplyDraftRequest, ReplyDraftResponse, ThreadSummaryResponse
from app.services.ai.pipeline import analyze_email, generate_reply_draft, summarize_thread_messages

router = APIRouter()


@router.post("/analyze/{email_id}")
async def run_email_analysis(
    email_id: uuid.UUID,
    provider: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger full AI analysis (summarization, categorization, priority, actions) for an email."""
    query = select(EmailMessage).where(
        EmailMessage.id == email_id,
        EmailMessage.user_id == current_user.id,
    )
    result = await db.execute(query)
    message = result.scalar_one_or_none()

    if message is None:
        raise HTTPException(status_code=404, detail="Email message not found")

    analysis = await analyze_email(message, db, provider_name=provider)
    return {
        "id": analysis.id,
        "message_id": analysis.message_id,
        "summary": analysis.summary,
        "category": analysis.category,
        "priority": analysis.priority,
        "action_items": analysis.action_items,
        "confidence_score": analysis.confidence_score,
        "ai_provider": analysis.ai_provider,
        "model_used": analysis.model_used,
        "created_at": analysis.created_at,
    }


@router.get("/analysis/{email_id}")
async def get_email_analysis(
    email_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the cached AI analysis for a specific email."""
    query = select(AIAnalysis).where(
        AIAnalysis.message_id == email_id,
        AIAnalysis.user_id == current_user.id,
    )
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(status_code=404, detail="No AI analysis found for this email")

    return {
        "id": analysis.id,
        "message_id": analysis.message_id,
        "summary": analysis.summary,
        "category": analysis.category,
        "priority": analysis.priority,
        "action_items": analysis.action_items,
        "confidence_score": analysis.confidence_score,
        "ai_provider": analysis.ai_provider,
        "model_used": analysis.model_used,
        "created_at": analysis.created_at,
    }


@router.post("/reply-draft", response_model=ReplyDraftResponse)
async def create_reply_draft(
    payload: ReplyDraftRequest,
    provider: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate an AI reply draft with a selected tone (professional, formal, friendly, concise)."""
    query = select(EmailMessage).where(
        EmailMessage.id == payload.email_id,
        EmailMessage.user_id == current_user.id,
    )
    result = await db.execute(query)
    message = result.scalar_one_or_none()

    if message is None:
        raise HTTPException(status_code=404, detail="Email message not found")

    draft_text = await generate_reply_draft(
        message=message,
        tone=payload.tone,
        instructions=payload.instructions,
        provider_name=provider,
    )

    return ReplyDraftResponse(draft=draft_text, tone=payload.tone)


@router.get("/thread-summary/{thread_id}", response_model=ThreadSummaryResponse)
async def get_thread_summary(
    thread_id: uuid.UUID,
    provider: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Summarize an entire multi-message email thread."""
    t_query = select(EmailThread).where(
        EmailThread.id == thread_id,
        EmailThread.user_id == current_user.id,
    )
    t_res = await db.execute(t_query)
    thread = t_res.scalar_one_or_none()

    if thread is None:
        raise HTTPException(status_code=404, detail="Email thread not found")

    m_query = (
        select(EmailMessage)
        .where(
            EmailMessage.thread_id == thread.id,
            EmailMessage.user_id == current_user.id,
        )
        .order_by(EmailMessage.timestamp.asc().nullslast())
    )
    m_res = await db.execute(m_query)
    messages = list(m_res.scalars().all())

    summary_text = await summarize_thread_messages(
        thread=thread,
        messages=messages,
        provider_name=provider,
    )

    return ThreadSummaryResponse(
        thread_id=thread.id,
        summary=summary_text,
        message_count=len(messages),
    )


@router.get("/usage")
async def get_ai_usage_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get AI usage statistics and total estimated token counts."""
    query = (
        select(
            AIUsageLog.feature,
            AIUsageLog.provider,
            func.count(AIUsageLog.id).label("total_calls"),
            func.sum(AIUsageLog.tokens_used).label("total_tokens"),
        )
        .where(AIUsageLog.user_id == current_user.id)
        .group_by(AIUsageLog.feature, AIUsageLog.provider)
    )
    result = await db.execute(query)
    rows = result.all()

    breakdown = [
        {
            "feature": r.feature,
            "provider": r.provider,
            "total_calls": r.total_calls,
            "total_tokens": r.total_tokens or 0,
        }
        for r in rows
    ]

    return {"usage": breakdown}
