## 1. Entorno de Backend (FastAPI)

1. **Creación del entorno virtual:**
    
    - Comando: `python -m venv venv`
        
    - Uso: Aislar las dependencias del proyecto de la instalación global.
        
2. **Instalación de dependencias base:**
    
    - Comando: `pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary passlib python-jose`
        
    - **FastAPI:** Framework web principal asíncrono.
        
    - **SQLAlchemy:** ORM para interactuar con la base de datos mediante objetos Python.
        
    - **Alembic:** Gestor de migraciones para la base de datos.
        
    - **psycopg2-binary:** Driver de PostgreSQL.
        

## 2. Configuración Multi-tenant (Esquema Compartido)

A diferencia de separar por esquemas físicos de BD, este proyecto utiliza un **Shared Schema**.

1. **Lógica de Aislamiento:**
    
    - Todos los clientes/talleres comparten las mismas tablas.
        
    - El aislamiento se logra mediante la columna `taller_id` presente en las tablas principales (`Usuario`, `Incidente`, `Pago`).
        
2. **Implementación en FastAPI:**
    
    - Se extrae el `taller_id` del Token JWT del usuario autenticado a través de una Dependencia (`Depends(get_current_user)`).
        
    - Ese ID se pasa obligatoriamente a los repositorios CRUD para aplicar un filtro `WHERE taller_id = X` en todas las consultas.
        

## 3. Seguridad y API

1. **Autenticación (JWT & Bcrypt):**
    
    - Se utiliza `passlib` para hashear las contraseñas antes de guardarlas (cumpliendo con límites de 72 bytes).
        
    - Se generan JSON Web Tokens (JWT) con `python-jose` que contienen la identidad del usuario y su rol.
        
2. **CORS (Cross-Origin Resource Sharing):**
    
    - Configurado en `app/main.py` mediante `CORSMiddleware` para permitir peticiones desde el origen del frontend (puerto 3000 o 5173).
        

## 4. Integridad Referencial (Hardening de Base de Datos)

El esquema de base de datos ha sido reforzado mediante directivas en SQLAlchemy (`app/models/`):

- **RESTRICT:** Aplicado en llaves foráneas críticas (`usuario_id`, `vehiculo_id` en `Incidente`) para evitar datos huérfanos y mantener trazabilidad.
    
- **CASCADE:** Aplicado en dependencias de configuración (`HorarioTaller`, `TokenDispositivo`) para limpieza automática.
    
- **SET NULL:** Aplicado en relaciones operativas (asignación de mecánicos a incidentes) para permitir reasignaciones si un empleado es dado de baja.