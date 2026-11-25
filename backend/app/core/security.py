import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def get_fernet() -> Fernet:
    """Generate a stable 32-byte urlsafe Fernet key derived from SECRET_KEY."""
    derived_key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    urlsafe_key = base64.urlsafe_b64encode(derived_key)
    return Fernet(urlsafe_key)


def encrypt_token(plain_token: str) -> str:
    """Encrypt sensitive OAuth tokens before storing in the database."""
    if not plain_token:
        return ""
    f = get_fernet()
    return f.encrypt(plain_token.encode()).decode()


def decrypt_token(cipher_token: str) -> str:
    """Decrypt sensitive OAuth tokens retrieved from the database."""
    if not cipher_token:
        return ""
    f = get_fernet()
    return f.decrypt(cipher_token.encode()).decode()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
