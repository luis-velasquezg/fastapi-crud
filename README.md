# FastAPI CRUD

Aplicación sencilla de FastAPI que muestra operaciones CRUD básicas con una API RESTful.

## 📦 Características

- Operaciones de creación, lectura, actualización y eliminación (CRUD)
- Modelos Pydantic para la validación de datos

## 👤 Modelo de Usuario

### Campos de Usuario

- `id`: Identificación
- `nombre`: Nombre del usuario _(entre 2 y 50 caracteres)_
- `email`: Correo electrónico válido
- `telefono`: Teléfono _(entre 7 y 15 dígitos)_
- `edad`: Edad _(entre 0 y 120 años)_

### Modelos de usuario:

1. `UsuarioBase`: Modelo base con validaciones predeterminadas y personalizadas
2. `UsuarioCreate`: Modelo para crear un nuevo usuario
3. `UsuarioUpdate`: MModelo para actualizar un usuario existente
4. `Usuario`: Modelo base con ID

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
