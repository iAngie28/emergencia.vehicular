import os
import sys
import subprocess
from sqlalchemy import create_engine, text
# Asegurar que encuentre el módulo 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base  # Asegúrate de que este archivo importe todos tus modelos
from app.db.session import SessionLocal, engine
from app.db.seeder import seed_db 
from app.core.config import settings

def run_command(command):
    """Ejecuta comandos de terminal"""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Nota/Error: {result.stderr}")
    else:
        print(f"✅ Éxito: {result.stdout}")

def reset_database():
    DATABASE_URL = settings.DATABASE_URL
    print(f"🚀 --- INICIANDO RESET TOTAL EN: {DATABASE_URL.split('@')[-1]} ---")

    # 1. Limpieza de Esquema (Bomba Atómica)
    try:
        with engine.connect() as conn:
            print("🧹 Borrando y recreando esquema público...")
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.commit()
        print("✅ Esquema limpio.")
    except Exception as e:
        print(f"❌ Error al limpiar DB: {e}")
        return

    # 2. Reconstruir Tablas mediante SQLAlchemy
    print("🏗️ Creando tablas desde modelos de SQLAlchemy...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return

    # 3. Sincronizar Alembic (Stamp)
    # Esto le dice a Alembic que la DB ya está en la última versión y no intente crear tablas de nuevo
    print("🔖 Marcando versión en Alembic (Stamp)...")
    run_command("alembic stamp head")

    # 4. Ejecutar Seeder 🌱
    print("🌱 Poblando base de datos...")
    db = SessionLocal()
    try:
        seed_db(db)
        print("✅ Datos de prueba insertados.")

        # 5. Sincronizar Secuencias de IDs (PostgreSQL)
        print("🔄 Sincronizando secuencias...")
        with engine.connect() as conn:
            # Lista de tablas a sincronizar
            tablas = ['rol', 'usuario', 'taller', 'incidente', 'pago', 'especialidad', 'evidencia', 'bitacora']
            for tabla in tablas:
                try:
                    # Intenta sincronizar la secuencia de la tabla
                    conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM {tabla};"))
                except Exception:
                    continue
            conn.commit()
        print("✅ Secuencias alineadas.")
    except Exception as e:
        print(f"❌ Error en el Seeder: {e}")
    finally:
        db.close()

    print("\n✨ ¡SISTEMA LISTO Y DESPLEGADO! ✨")

if __name__ == "__main__":
    # Si detecta RENDER o entorno no interactivo, procede sin preguntar
    IS_RENDER = os.environ.get("RENDER") or os.environ.get("DATABASE_URL")
    
    if IS_RENDER:
        reset_database()
    else:
        confirm = input("⚠️ ¿Borrar TODA la base de datos local? (s/n): ")
        if confirm.lower() == 's':
            reset_database()
        else:
            print("❌ Abortado.")