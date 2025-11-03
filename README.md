# FastAPI CRUD

Aplicación sencilla de FastAPI que muestra operaciones CRUD básicas con una API RESTful.

## 📦 Características

- Operaciones de creación, lectura, actualización y eliminación (CRUD)
- Modelos Pydantic para la validación de datos

## 👤 Modelo de Usuario

### Campos de Usuario

- `name`: Nombre del usuario
- `email`: Correo electrónico válido
- `password`: Contraseña segura _(mínimo 8 caracteres, que contenga mayúsculas, minúsculas y números)_
- `id`: Identificador único del usuario

### Modelos de usuario:

1. `UserBase`: Modelo base con validaciones comunes
2. `UserCreate`: Modelo para crear un nuevo usuario
3. `UserUpdate`: Modelo para actualizar un usuario existente
4. `User`: Modelo base con ID (sin contraseña)

## 🛠️ Instalación

```bash
git clone https://github.com/luis-velasquezg/fastapi-crud.git
cd fastapi-crud
pip install -r requirements.txt
```

## ▶️ Ejecución

Ejecutar el servidor en la terminal:

```bash
uvicorn main:app --reload
```

Abrir documentación de la API en un navegador:

```bash
http://127.0.0.1:8000/docs
```
