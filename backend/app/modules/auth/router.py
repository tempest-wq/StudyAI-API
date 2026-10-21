from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.auth.schemas import UserCreate, UserResponse
from app.modules.auth.service import EmailAlreadyRegisteredError, create_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    try:
        user = await create_user(session, user_data)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.") from exc

    return UserResponse.model_validate(user)
