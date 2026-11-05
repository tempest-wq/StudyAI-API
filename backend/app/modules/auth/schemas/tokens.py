from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    """Resposta de login e renovação de sessão."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    """Entrada da rota de renovação do refresh token."""
    refresh_token: str = Field(min_length=1)