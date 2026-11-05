from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.auth.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse
)
from app.modules.auth.services import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    create_user,
    authenticate_user
)
from app.modules.auth.dependencies import CurrentUser


router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    try:
        user = await create_user(session, user_data)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado.") from exc

    return UserResponse.model_validate(user)

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, session: AsyncSession = Depends(get_session)) -> TokenResponse:
    try:
        access_token, refresh_token = await authenticate_user(session, login_data)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exc

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse, name="Carrega as informações do usuário")
async def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)