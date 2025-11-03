from fastapi import FastAPI, HTTPException, status
from typing import List
from models import User, UserCreate, UserUpdate

app = FastAPI(title="Simple FastAPI CRUD", version="1.0")

# Base de datos temporal
users_db: List[User] = [
    User(id=1, name="María", email="maria@example.com"),
    User(id=2, name="Luis", email="luis@example.com"),
    User(id=3, name="Jose", email="jose@example.com"),
    User(id=4, name="Ana", email="ana@example.com"),
]
next_id = 5


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_id

    # Verificar que el email no esté repetido
    if any(u.email == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    new_user = User(id=next_id, name=user.name, email=user.email)
    users_db.append(new_user)
    next_id += 1
    return new_user


@app.get("/users", response_model=List[User])
def list_users():
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, data: UserUpdate):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    if data.email and any(u.email == data.email and u.id != user_id for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya en uso"
        )

    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    users_db = [u for u in users_db if u.id != user_id]
