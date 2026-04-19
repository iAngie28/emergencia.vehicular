import os
import subprocess
from sqlalchemy import create_engine, text
from app.db.session import SessionLocal 
from app.db.seeder import seed_db
# --- CONFIGURACIÓN ---
# Reemplaza con tus datos reales
DB_USER = "postgres"
DB_PASS = "adm123" # <--- Pon tu contraseña aquí
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "emergencias_db" # <--- Pon el nombre de tu DB aquí

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_command(command):
    """Ejecuta un comando de consola y muestra la salida"""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    else:
        print(f"✅ Éxito: {result.stdout}")

def reset_database():
    print("🚀 --- INICIANDO RESETEO TOTAL ---")
    
    # 1. Limpiar la Base de Datos físicamente
    try:
        engine = create_engine(DATABASE_URL)
        print("🧹 Borrando esquema público...")
        with engine.connect() as conn:
            # Terminamos conexiones activas para que nos deje borrar el esquema
            conn.execute(text("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = current_database()
                  AND pid <> pg_backend_pid();
            """))
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.commit()
        print("✅ Base de datos limpia (Schema public recreado).")
    except Exception as e:
        print(f"❌ Error conectando a la DB: {e}")
        return

    # 2. Borrar archivos de versiones de Alembic
    # Intentamos ambas rutas comunes por si acaso
    versions_dir = "app/alembic/versions" if os.path.exists("app/alembic") else "alembic/versions"
    
    if os.path.exists(versions_dir):
        print(f"📂 Limpiando carpeta: {versions_dir}")
        for filename in os.listdir(versions_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                file_path = os.path.join(versions_dir, filename)
                os.remove(file_path)
        print("✅ Versiones físicas eliminadas.")
    else:
        print(f"⚠️ No se encontró la carpeta de versiones en {versions_dir}")

    # 3. Generar y Aplicar Migraciones
    print("⚙️ Generando nueva migración inicial...")
    run_command("python -m alembic revision --autogenerate -m 'Initial_Reset'")
    
    print("📈 Aplicando migración a la DB...")
    run_command("python -m alembic upgrade head")
    
    print("\n✨ ¡PROCESO COMPLETADO CON ÉXITO! ✨")
    print("Ya puedes iniciar uvicorn y probar tu Swagger.")

    print("🌱 Ejecutando el Seeder para poblar la base de datos...")
    db_session = SessionLocal()
    try:
        seed_db(db_session)
        print("✅ Base de datos poblada exitosamente.")
        # Dentro de reset_database(), después de seed_db(db_session)
        try:
            print("🔄 Sincronizando secuencias de IDs...")
            with engine.connect() as conn:
                conn.execute(text("SELECT setval('taller_id_seq', (SELECT MAX(id) FROM taller));"))
                conn.execute(text("SELECT setval('usuario_id_seq', (SELECT MAX(id) FROM usuario));"))
                conn.commit()
            print("✅ Secuencias sincronizadas.")
        except Exception as e:
            print(f"⚠️ Nota: No se pudo sincronizar secuencias (esto es normal si no hay datos aún): {e}")
    except Exception as e:
        print(f"❌ Error al ejecutar el seeder: {e}")
    finally:
        db_session.close()

    print("\n✨ ¡PROCESO COMPLETADO CON ÉXITO! ✨")
    print("La base de datos está reseteada, migrada y con datos semilla.")
    print("Ya puedes iniciar uvicorn y probar tu Swagger.")
    
if __name__ == "__main__":
    reset_database()

    