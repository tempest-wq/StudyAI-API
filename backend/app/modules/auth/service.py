from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate
from app.modules.auth.security import hash_password

class EmailAlreadyRegisteredError(Exception):
    """Lança exception de email já utilizado"""

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