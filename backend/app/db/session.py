import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from typing import Generator

# 1. Cargar variables de entorno desde .env
# Buscar el archivo .env en el directorio del backend
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=str(env_path))

# 2. Obtener la URL de la base de datos del archivo .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Si no encuentra en .env, usar SQLite como fallback
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./emergencias.db"

# 3. Crear el Engine (Motor de conexión)
# 'pool_pre_ping' ayuda a reconectar si la base de datos se reinicia
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 4. Configurar la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Dependencia para FastAPI (Inyección de Dependencias)
# Esta es la función que usarás en tus rutas (endpoints)
def get_db() -> Generator[Session, None, None]:
    """
    Crea una nueva sesión de base de datos para cada petición y 
    la cierra automáticamente al terminar, incluso si hay errores.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()