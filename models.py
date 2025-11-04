import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


class ValidacionesComunes(BaseModel):
    """Clase base para validaciones comunes."""

    @classmethod
    def validar_nombre(cls, value: str) -> str:
        """Regla común: nombre válido."""
        value = str(value).strip()
        min_length = 2
        max_length = 50

        if len(value) < min_length or len(value) > max_length:
            raise ValueError(
                f"El nombre debe tener entre {min_length} y {max_length} caracteres."
            )
        if re.search(r"[0-9!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "El nombre no puede contener números o caracteres especiales"
            )
        return value

    @classmethod
    def validar_edad(cls, value: Optional[int]) -> Optional[int]:
        """Regla común: edad válida si se proporciona."""
        edad_min = 0
        edad_max = 120

        if value is not None:
            if value < edad_min or value > edad_max:
                raise ValueError(
                    f"La edad debe estar entre {edad_min} y {edad_max} años."
                )
        return value

    @classmethod
    def validar_telefono(cls, value: Optional[str]) -> Optional[str]:
        """Regla común: teléfono válido si se proporciona."""
        if value is not None:
            value = str(value).strip()
            min_length = 7
            max_length = 15

            if len(value) < min_length or len(value) > max_length:
                raise ValueError(
                    f"El teléfono debe tener entre {min_length} y {max_length} caracteres."
                )
        return value


class UsuarioBase(BaseModel):
    # Habilitar validación en asignaciones
    model_config = ConfigDict(validate_assignment=True)

    nombre: str = Field(..., description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: Optional[str] = Field(None, description="Número de teléfono")
    edad: Optional[int] = Field(None, ge=0, le=120, description="Edad del usuario")

    _validar_nombre = field_validator("nombre")(ValidacionesComunes.validar_nombre)
    _validar_edad = field_validator("edad")(ValidacionesComunes.validar_edad)
    _validar_telefono = field_validator("telefono")(
        ValidacionesComunes.validar_telefono
    )


class UsuarioCreate(UsuarioBase):
    """Modelo para creación - campos obligatorios"""

    model_config = ConfigDict(
        validate_assignment=True,
    )

    @field_validator("nombre", "email")
    @classmethod
    def validar_campos_obligatorios(cls, value, info):

        if not value or str(value).strip() == "":
            raise ValueError(
                f"El campo '{info.field_name}' es obligatorio y no puede estar vacío."
            )
        return str(value).strip()


class UsuarioUpdate(UsuarioBase):
    """
    Modelo para actualizaciones parciales.
    Todos los campos son opcionales pero mantienen sus validaciones.
    """

    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    edad: Optional[int] = None

    model_config = ConfigDict(validate_assignment=True)


class Usuario(UsuarioBase):
    id: int
