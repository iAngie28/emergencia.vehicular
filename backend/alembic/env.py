import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 🚀 NUEVO: Cargar variables locales del archivo .env
from dotenv import load_dotenv
load_dotenv()

from app.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    if not url:
        url = config.get_main_option("sqlalchemy.url")
        
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 1. Obtener la URL de la variable de entorno de Render o de tu .env local
    url = os.getenv("DATABASE_URL")
    
    # 2. Fallback: Si no hay variable, intenta sacarla del archivo alembic.ini
    if not url:
        url = config.get_main_option("sqlalchemy.url")
        
    # 3. Fix para PostgreSQL en Render
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    # 4. Protección contra el error "Expected string or URL object, got None"
    if not url:
        raise ValueError("❌ No se encontró DATABASE_URL. Revisa que tu archivo .env exista y tenga la variable.")

    # 5. Inyectar la URL correcta en la configuración de Alembic
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        configuration = {}
    configuration["sqlalchemy.url"] = url 

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()