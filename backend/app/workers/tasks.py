from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def sync_email_account(self, account_id: str):
    """Sync emails for a given account."""
    try:
        # TODO: Implement email sync via Gmail API
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def process_email_ai(self, message_id: str):
    """Run AI processing (summarize, classify, prioritize) on an email."""
    try:
        # TODO: Implement AI processing pipeline
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def generate_embedding(self, message_id: str):
    """Generate and store embedding for semantic search."""
    try:
        # TODO: Implement embedding generation with pgvector storage
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=2)
def generate_daily_digest(self, user_id: str):
    """Generate daily digest for a specific user."""
    try:
        # TODO: Implement daily digest generation
        pass
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task
def generate_daily_digest_all():
    """Triggered by beat — dispatches per-user digest tasks."""
    # TODO: Query all users with digest enabled and dispatch per-user tasks
    pass
