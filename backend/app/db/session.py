import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from typing import Generator

# 1. Cargar variables de entorno
load_dotenv()

# 2. Obtener la URL de la base de datos del archivo .env
# Ejemplo: postgresql://user:password@localhost:5432/emergencias_db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está configurada en el archivo .env")

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