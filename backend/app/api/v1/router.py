from fastapi import APIRouter

from app.api.v1 import auth, accounts, emails, ai, actions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
