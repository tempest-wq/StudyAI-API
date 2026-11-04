from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.modules.auth.models import User, RefreshToken
from app.modules.auth.schemas import UserCreate, LoginRequest
from app.modules.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token
)

class EmailAlreadyRegisteredError(Exception):
    """Email já cadastrado"""

class InvalidCredentialsError(Exception):
    """Credenciais de autenticação inválidas"""


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    email = str(user_data.email)

    existing_user = await session.scalar(select(User).where(User.email == email))

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    user = User(full_name=user_data.full_name, email=email, password_hash=hash_password(user_data.password))
    session.add(user)

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise EmailAlreadyRegisteredError from exc

    await session.refresh(user)
    return user

async def authenticate_user(session: AsyncSession, login_data: LoginRequest) -> tuple[str, str]:
    email = str(login_data.email)

    user = await session.scalar(
        select(User).where(User.email == email)
    )

    if user is None:
        raise InvalidCredentialsError

    if not verify_password(login_data.password, user.password_hash):
        raise InvalidCredentialsError

    if not user.is_active:
        raise InvalidCredentialsError

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
    )

    session.add(refresh_token_record)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise

    return access_token, refresh_token
