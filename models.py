from pydantic import BaseModel, EmailStr, Field, validator
import re
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=50, description="Nombre del usuario"
    )
    email: EmailStr = Field(..., description="Correo electrónico válido")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Contraseña con mínimo 8 caracteres",
    )

    @validator("password")
    def validate_password(cls, value):
        # Requisitos mínimos de complejidad
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una letra minúscula."
            )
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        return value


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class User(UserBase):
    id: int
