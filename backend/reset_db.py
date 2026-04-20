import os
import subprocess
from sqlalchemy import create_engine, text
from app.db.session import SessionLocal 
from app.db.seeder import seed_db  # <--- Tu archivo de semillas
from app.core.config import settings

def run_command(command):
    """Ejecuta comandos de terminal (Alembic)"""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    else:
        print(f"✅ Éxito: {result.stdout}")

def reset_database():
    # 1. Obtener URL de Render o Local automáticamente
    DATABASE_URL = settings.DATABASE_URL
    print(f"🚀 --- INICIANDO PROCESO EN: {DATABASE_URL.split('@')[-1]} ---")

    # 2. Limpiar Base de Datos (Bomba Atómica)
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("🧹 Borrando esquema público...")
            # Cortar conexiones para que Postgres nos deje borrar
            conn.execute(text("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = current_database()
                  AND pid <> pg_backend_pid();
            """))
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.commit()
        print("✅ Base de datos vaciada.")
    except Exception as e:
        print(f"❌ Error al limpiar DB: {e}")
        return

    # 3. Limpiar archivos de Alembic locales
    # Esto evita el error de "Can't locate revision"
    versions_dir = "app/alembic/versions" if os.path.exists("app/alembic") else "alembic/versions"
    if os.path.exists(versions_dir):
        print(f"📂 Limpiando carpeta de versiones: {versions_dir}")
        for filename in os.listdir(versions_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                os.remove(os.path.join(versions_dir, filename))

    # 4. Reconstruir Tablas (Alembic)
    print("⚙️ Generando nueva migración inicial...")
    run_command("python -m alembic revision --autogenerate -m 'Initial_Reset'")
    print("📈 Aplicando tablas a la DB...")
    run_command("python -m alembic upgrade head")

    # 5. LLAMADA AL SEEDER 🌱
    print("🌱 Ejecutando Seeder para poblar datos...")
    db = SessionLocal()
    try:
        seed_db(db) # <--- Aquí es donde ocurre la magia de insertar talleres/usuarios
        print("✅ Datos de prueba insertados con éxito.")

        # 6. Sincronizar Secuencias
        # (Esto es vital para que no falle el próximo registro manual)
        print("🔄 Sincronizando contadores (Sequences)...")
        with engine.connect() as conn:
            tablas = ['rol', 'usuario', 'taller', 'incidente', 'pago'] # Ajusta según tus tablas
            for tabla in tablas:
                try:
                    conn.execute(text(f"SELECT setval('{tabla}_id_seq', (SELECT MAX(id) FROM {tabla}));"))
                except:
                    continue
            conn.commit()
        print("✅ Secuencias alineadas.")

    except Exception as e:
        print(f"❌ Error en el Seeder: {e}")
    finally:
        db.close()

    print("\n✨ ¡SISTEMA RESETEADO Y POBLADO! ✨")
    print("Ya puedes usar tus credenciales del seeder para entrar.")

if __name__ == "__main__":
    # Seguridad: Si no es localhost, pedir confirmación
    if "localhost" not in settings.DATABASE_URL and "127.0.0.1" not in settings.DATABASE_URL:
        confirm = input("⚠️ ¡ESTÁS APUNTANDO A RENDER! ¿Borrar todo? (s/n): ")
        if confirm.lower() == 's':
            reset_database()
        else:
            print("❌ Abortado.")
    else:
        reset_database()