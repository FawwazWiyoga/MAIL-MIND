import asyncio
import logging

from app.workers.celery_app import celery_app
from app.services.sync import sync_account_emails

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


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def process_email_ai(self, message_id: str):
    """Run AI processing (summarize, classify, prioritize) on an email."""
    try:
        # Placeholder for Phase 3 AI extraction
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def generate_embedding(self, message_id: str):
    """Generate and store embedding for semantic search."""
    try:
        # Placeholder for Phase 4 Semantic Search
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2)
def generate_daily_digest(self, user_id: str):
    """Generate daily digest for a specific user."""
    try:
        # Placeholder for Phase 5 Daily Digest
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def generate_daily_digest_all():
    """Triggered by beat — dispatches per-user digest tasks."""
    pass
