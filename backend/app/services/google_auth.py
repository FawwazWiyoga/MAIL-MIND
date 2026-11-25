import json
import urllib.parse
from datetime import datetime, timezone, timedelta
import httpx

from app.core.config import get_settings

settings = get_settings()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

GMAIL_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def get_google_auth_url(user_id: str, redirect_uri: str | None = None) -> str:
    """Generate the Google OAuth consent URL with state parameter holding user ID."""
    target_redirect_uri = redirect_uri or settings.GOOGLE_REDIRECT_URI
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": target_redirect_uri,
        "response_type": "code",
        "scope": " ".join(GMAIL_SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": user_id,
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


async def exchange_google_code(code: str, redirect_uri: str | None = None) -> dict:
    """
    Exchange the authorization code with Google for tokens and fetch user email.
    Returns:
        dict with access_token, refresh_token, token_expiry, email
    """
    target_redirect_uri = redirect_uri or settings.GOOGLE_REDIRECT_URI

    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": target_redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_res = await client.post(GOOGLE_TOKEN_URL, data=payload)
        if token_res.status_code != 200:
            raise ValueError(f"Failed to exchange code: {token_res.text}")
        token_data = token_res.json()

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in", 3600)
        token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        # Fetch user's Gmail address from userinfo
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_res = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        if userinfo_res.status_code != 200:
            raise ValueError(f"Failed to fetch userinfo: {userinfo_res.text}")
        userinfo = userinfo_res.json()
        email_address = userinfo.get("email")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_expiry": token_expiry,
        "email_address": email_address,
    }
