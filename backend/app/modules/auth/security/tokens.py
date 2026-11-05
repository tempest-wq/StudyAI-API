from datetime import datetime, timezone, timedelta
from uuid import UUID
import hashlib
import jwt

from app.core.config import settings

"""Criação, validação e hash dos tokens de autenticação."""
class InvalidAccessTokenError(Exception):
    """Token de acesso inválido"""

class InvalidRefreshTokenError(Exception):
    """Token de renovação inválido"""

def _create_token(subject: UUID, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def create_access_token(subject: UUID) -> str:
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

def create_refresh_token(subject: UUID) -> str:
    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days
        )
    )

def decode_access_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError as exc:
        raise InvalidAccessTokenError from exc

    if payload.get("type") != "access":
        raise InvalidAccessTokenError

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise InvalidAccessTokenError

    try:
        return UUID(subject)
    except ValueError as exc:
        raise InvalidAccessTokenError from exc

def decode_refresh_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError as exc:
        raise InvalidRefreshTokenError from exc

    if payload.get("type") != "refresh":
        raise InvalidRefreshTokenError

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise InvalidRefreshTokenError

    try:
        return UUID(subject)
    except ValueError as exc:
        raise InvalidRefreshTokenError from exc

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()