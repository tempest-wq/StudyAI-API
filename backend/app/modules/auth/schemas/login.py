from pydantic import BaseModel, EmailStr, field_validator

class LoginRequest(BaseModel):
    """Entrada da rota de autenticação do usuário."""
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()