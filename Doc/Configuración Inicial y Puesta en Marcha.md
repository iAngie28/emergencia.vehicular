Sigue estos pasos para levantar el entorno de desarrollo del SaaS de Asistencia Vehicular Multi-tenant.

## 🎯 Requisitos Previos

- **PostgreSQL** instalado y corriendo en `localhost:5432`.
    
- **Python 3.13** instalado.
    
- **Node.js 18+** instalado (para el frontend).
    
- Base de datos creada (ej. **`asistencia_vehicular_db`**) con credenciales conocidas.
    

## 📋 Paso 1: Configurar el Backend (FastAPI)

### 1.1 Activar entorno virtual

**En Windows (PowerShell):**

```
.\venv\Scripts\Activate.ps1
```

### 1.2 Instalar dependencias

```
pip install -r requirements.txt
```

### 1.3 Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del backend con:

```
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/asistencia_vehicular_db
SECRET_KEY=tu_clave_secreta_jwt
OPENAI_API_KEY=tu_api_key_para_ia
```

### 1.4 Resetear y Poblar la Base de Datos

Utiliza el script maestro para limpiar la base de datos, aplicar migraciones e inyectar las reglas de integridad referencial (CASCADE, RESTRICT):

```
python reset_db.py
```

### 1.5 Iniciar el Servidor de Desarrollo

```
uvicorn app.main:app --reload
```

_FastAPI estará disponible en `http://localhost:8000` y el Swagger UI en `http://localhost:8000/docs`._

## 🎨 Paso 2: Configurar el Frontend

### 2.1 Instalar dependencias

```
cd frontend
npm install
```

### 2.2 Iniciar servidor de desarrollo

```
npm run dev
```

_El Frontend iniciará en el puerto configurado (ej. `http://localhost:5173` o `3000`)._

## 🧹 Operaciones de Mantenimiento (Backend)

### Crear una nueva migración (si modificas `models/`)

```
python -m alembic revision --autogenerate -m "descripcion_del_cambio"
```

### Aplicar migraciones pendientes

```
python -m alembic upgrade head
```