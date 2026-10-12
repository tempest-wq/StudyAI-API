from uuid import UUID

from pydantic import (BaseModel,
                      Field,
                      ConfigDict,
                      EmailStr,
                      field_validator)
"""
    Contrato do cadastro
"""
class UserCreate(BaseModel):
    full_name: str = Field(min_length=5, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value:str) -> str :
        return value.strip().lower()

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr