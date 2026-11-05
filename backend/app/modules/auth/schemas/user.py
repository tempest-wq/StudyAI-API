from uuid import UUID

from pydantic import (BaseModel,
                      ConfigDict,
                      EmailStr,
                      field_validator,
                      Field
                      )

class UserCreate(BaseModel):
    """Entrada da rota de cadastro de usuário"""
    full_name: str = Field(min_length=5, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value:str) -> str :
        return value.strip().lower()

class UserResponse(BaseModel):
    """Dados públicos retornados sobre um usuário"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr