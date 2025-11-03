from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Modelos de usuario:
# 1. UserBase: Modelo base con validaciones comunes
# 2. UserCreate: Modelo para crear un nuevo usuario
# 3. UserUpdate: Modelo para actualizar un usuario existente
# 4. User: Modelo completo con ID


class UserBase(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=50, description="Nombre del usuario"
    )
    email: EmailStr = Field(..., description="Correo electrónico válido")


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=6, description="Contraseña con mínimo 6 caracteres"
    )


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


class User(UserBase):
    id: int
