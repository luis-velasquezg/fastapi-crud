from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Usuario, UsuarioBase, UsuarioCreate, UsuarioUpdate

app = FastAPI(title="FastAPI CRUD", version="1.0")

# Base de datos temporal
usuarios: List[Usuario] = [
    Usuario(
        id=1, nombre="María", email="maria@example.com", telefono="123456789", edad=24
    ),
    Usuario(
        id=2, nombre="Luis", email="luis@example.com", telefono="987654321", edad=35
    ),
    Usuario(
        id=3, nombre="Jose", email="jose@example.com", telefono="456789123", edad=40
    ),
    Usuario(id=4, nombre="Ana", email="ana@example.com", telefono="321654987"),
]
contador_id = 5


@app.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    global contador_id

    # Verificar que el email no esté repetido
    if any(u.email == usuario.email for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    nuevo_usuario = Usuario(
        id=contador_id,
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono,
        edad=usuario.edad,
    )
    usuarios.append(nuevo_usuario)
    contador_id += 1
    return nuevo_usuario


@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios


@app.get("/usuarios/{id}", response_model=Usuario)
def obtener_usuario(id: int):
    usuario = next((u for u in usuarios if u.id == id), None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return usuario


@app.put("/usuarios/{id}", response_model=Usuario)
def actualizar_usuario(id: int, datos: UsuarioUpdate):
    """
    Actualiza un usuario existente.

    Mejoras implementadas:
    - Usa model_copy() con update para mantener validaciones de Pydantic
    - Valida email único antes de aplicar cambios
    - exclude_unset=True solo incluye campos que el cliente envió explícitamente
    """
    # usuario = next((u for u in usuarios if u.id == id), None)

    # Buscar el usuario
    indice = next((i for i, u in enumerate(usuarios) if u.id == id), None)
    if indice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    usuario_actual = usuarios[indice]

    # Validar email único si se está actualizando
    if datos.email and any(u.email == datos.email and u.id != id for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya en uso"
        )

    # Obtener solo los campos que fueron enviados (exclude_unset=True)
    actualizaciones = datos.model_dump(exclude_unset=True)

    # Usar model_copy con update para mantener validaciones de Pydantic
    # Esto crea una nueva instancia validada en lugar de mutar directamente
    try:
        usuario_actualizado = usuario_actual.model_copy(update=actualizaciones)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {str(e)}",
        )

    # Reemplazar en la lista (simulando UPDATE de base de datos)
    usuarios[indice] = usuario_actualizado

    return usuario_actualizado


@app.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id: int):
    global usuarios
    usuario = next((u for u in usuarios if u.id == id), None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    usuarios = [u for u in usuarios if u.id != id]
