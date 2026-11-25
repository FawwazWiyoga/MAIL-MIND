import base64
from datetime import datetime, timezone
import re
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.core.config import get_settings

settings = get_settings()


def build_gmail_service(access_token: str, refresh_token: str | None = None):
    """Build an authorized Gmail API resource client."""
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def decode_base64url(data: str) -> str:
    """Decode Gmail base64url encoded string safely."""
    if not data:
        return ""
    try:
        padded = data + "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")
    except Exception:
        return ""


def extract_parts_content(payload: dict) -> tuple[str, str]:
    """Recursively extract plain text and HTML bodies from Gmail message payload."""
    body_text = ""
    body_html = ""

    mime_type = payload.get("mimeType", "")
    parts = payload.get("parts", [])

    if mime_type == "text/plain" and "data" in payload.get("body", {}):
        body_text += decode_base64url(payload["body"]["data"])
    elif mime_type == "text/html" and "data" in payload.get("body", {}):
        body_html += decode_base64url(payload["body"]["data"])

    for part in parts:
        sub_text, sub_html = extract_parts_content(part)
        if sub_text:
            body_text += "\n" + sub_text
        if sub_html:
            body_html += "\n" + sub_html

    return body_text.strip(), body_html.strip()


def parse_gmail_message(raw_msg: dict) -> dict[str, Any]:
    """Parse raw Gmail message format='full' into standard MailMind dictionary."""
    msg_id = raw_msg["id"]
    thread_id = raw_msg["threadId"]
    snippet = raw_msg.get("snippet", "")
    label_ids = raw_msg.get("labelIds", [])

    # Milliseconds internal date to UTC datetime
    internal_date_ms = int(raw_msg.get("internalDate", 0))
    msg_timestamp = (
        datetime.fromtimestamp(internal_date_ms / 1000, tz=timezone.utc)
        if internal_date_ms > 0
        else datetime.now(timezone.utc)
    )

    payload = raw_msg.get("payload", {})
    headers_list = payload.get("headers", [])
    headers = {h["name"].lower(): h["value"] for h in headers_list if "name" in h and "value" in h}

    subject = headers.get("subject", "(No Subject)")
    from_header = headers.get("from", "")
    to_header = headers.get("to", "")

    # Parse sender name and email from "Name <email@example.com>" format
    sender_name = from_header
    sender_email = from_header
    match = re.search(r"^(.*?)\s*<([^>]+)>$", from_header)
    if match:
        sender_name = match.group(1).strip().strip('"')
        sender_email = match.group(2).strip()

    # Parse recipients
    recipients = [r.strip() for r in to_header.split(",") if r.strip()] if to_header else []

    # Extract bodies
    body_text, body_html = extract_parts_content(payload)
    if not body_text and snippet:
        body_text = snippet

    is_read = "UNREAD" not in label_ids

    return {
        "provider_message_id": msg_id,
        "provider_thread_id": thread_id,
        "sender_name": sender_name or sender_email,
        "sender_email": sender_email,
        "recipient_emails": recipients,
        "subject": subject,
        "snippet": snippet,
        "body_text": body_text,
        "body_html": body_html or body_text,
        "timestamp": msg_timestamp,
        "is_read": is_read,
        "labels": label_ids,
    }
