import os
import sys
import subprocess
from sqlalchemy import create_engine, text

# CONFIGURAR ENCODING DE WINDOWS
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Asegurar que encuentre el módulo 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base  # Asegúrate de que este archivo importe todos tus modelos
from app.db.session import SessionLocal, engine
from app.db.seeder import seed_db 
from app.core.config import settings

# Manejo de errores encoding-safe
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_command(command):
    """Ejecuta comandos de terminal con mejor manejo de encoding"""
    print(f"[CMD] Executing: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.returncode != 0:
            stderr = (result.stderr[:200] if result.stderr else "Sin detalles").encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            print(f"[WARN] Error: {stderr}")
        else:
            stdout = (result.stdout[:200] if result.stdout else "Exito").encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            print(f"[OK] {stdout}")
    except Exception as e:
        error_str = str(e)[:100]
        error_str = error_str.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        print(f"[ERROR] Ejecutando comando: {error_str}")

def reset_database():
    DATABASE_URL = settings.DATABASE_URL
    is_sqlite = DATABASE_URL.startswith('sqlite')
    is_postgres = DATABASE_URL.startswith('postgresql')
    
    # Sanitizar la URL para evitar problemas de encoding
    db_info = DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL
    db_info = db_info.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    print(f"[INIT] --- INICIANDO RESET TOTAL EN: {db_info} ---")
    print(f"[INFO] Tipo de DB: {'SQLite' if is_sqlite else 'PostgreSQL'}")

    # 1. Limpieza de Esquema 
    try:
        if is_postgres:
            print("[CLEAN] Borrando y recreando esquema publico (PostgreSQL)...")
            with engine.connect() as conn:
                conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
                conn.execute(text("CREATE SCHEMA public;"))
                conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
                conn.commit()
        elif is_sqlite:
            print("[CLEAN] Limpiando base de datos SQLite...")
            db_path = DATABASE_URL.replace('sqlite:///', '').replace('sqlite:', '')
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"[OK] Archivo SQLite eliminado: {db_path}")
        print("[OK] Esquema limpio.")
    except Exception as e:
        # Evitar problemas de encoding en el mensaje de error
        try:
            error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
        except:
            error_msg = "[Error con encoding desconocido]"
        
        if "password" in error_msg.lower() or "auth" in error_msg.lower():
            print(f"[ERROR] ERROR DE AUTENTICACION con PostgreSQL")
            print(f"[ERROR] DATABASE_URL: {DATABASE_URL}")
        else:
            print(f"[WARN] Continuando a pesar del error en limpieza")
        # Continuamos de todas formas - talvez las tablas ya existen

    # 2. Reconstruir Tablas mediante SQLAlchemy
    print("[BUILD] Creando tablas desde modelos de SQLAlchemy...")
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Tablas creadas exitosamente.")
    except Exception as e:
        print(f"[ERROR] Error al crear tablas: {e}")
        return

    # 3. Sincronizar Alembic (Stamp)
    # Esto le dice a Alembic que la DB ya está en la última versión y no intente crear tablas de nuevo
    print("[STAMP] Marcando versión en Alembic (Stamp)...")
    run_command("alembic stamp head")

    # 4. Ejecutar Seeder
    print("[SEED] Poblando base de datos...")
    db = SessionLocal()
    try:
        seed_db(db)
        print("[OK] Datos de prueba insertados.")

        # 5. Sincronizar Secuencias de IDs (solo PostgreSQL)
        if is_postgres:
            print("[SYNC] Sincronizando secuencias (PostgreSQL)...")
            try:
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
                print("[OK] Secuencias alineadas.")
            except Exception as e:
                print(f"[WARN] Error al sincronizar secuencias: {str(e)[:100]}")
        else:
            print("[OK] SQLite no requiere sincronizacion de secuencias.")
    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        print(f"[ERROR] Error en el Seeder: {error_msg[:150]}")
    finally:
        db.close()

    print("\n[SUCCESS] SISTEMA LISTO Y DESPLEGADO!")

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