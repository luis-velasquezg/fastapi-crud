import re
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict,
    model_validator,
)
from typing import Optional


# # Validador compartido como función standalone
# def validar_nombre_sin_caracteres_especiales(value: Optional[str]) -> Optional[str]:
#     """Validador reutilizable para el campo nombre"""
#     if value is not None and re.search(r"[0-9!@#$%^&*(),.?\":{}|<>]", value):
#         raise ValueError("El nombre no puede contener números o caracteres especiales")
#     return value


class UsuarioBase(BaseModel):
    # Habilitar validación en asignaciones
    model_config = ConfigDict(validate_assignment=True)

    nombre: str = Field(
        ..., min_length=2, max_length=50, description="Nombre del usuario"
    )
    email: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: Optional[str] = Field(
        None, min_length=7, max_length=15, description="Número de teléfono"
    )
    edad: Optional[int] = Field(None, ge=0, le=120, description="Edad del usuario")

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value):
        if re.search(r"[0-9!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "El nombre no puede contener números o caracteres especiales"
            )
        return value

    # @field_validator("nombre", "email")
    # @classmethod
    # def validar_campos_obligatorios(cls, value, info):
    #     if not value or str(value).strip() == "":
    #         raise ValueError(
    #             f"El campo '{info.field_name}' es obligatorio y no puede estar vacío."
    #         )
    #     return value


class UsuarioCreate(UsuarioBase):
    """Modelo para creación - campos obligatorios"""

    model_config = ConfigDict(
        validate_assignment=True,
        # CLAVE: Esto hace que todos los campos heredados sean opcionales
        # sin tener que redefinirlos uno por uno
        fields={
            "nombre": {"default": None},
            "email": {"default": None},
            "telefono": {"default": None},
            "edad": {"default": None},
        },
    )

    @field_validator("nombre", "email")
    @classmethod
    def validar_campos_obligatorios(cls, value, info):
        if not value or str(value).strip() == "":
            raise ValueError(
                f"El campo '{info.field_name}' es obligatorio y no puede estar vacío."
            )
        return value


class UsuarioUpdate(UsuarioBase):
    """
    Modelo para actualizaciones parciales.
    Hereda TODOS los campos y validaciones de UsuarioBase,
    solo los hace opcionales usando model_config.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        # CLAVE: Esto hace que todos los campos heredados sean opcionales
        # sin tener que redefinirlos uno por uno
        fields={
            "nombre": {"default": None},
            "email": {"default": None},
            "telefono": {"default": None},
            "edad": {"default": None},
        },
    )


class Usuario(UsuarioBase):
    id: int
