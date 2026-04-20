from sqlalchemy import text
from app.db.session import engine

def limpiar():
    try:
        with engine.connect() as conn:
            # Borramos la tabla que tiene el historial viejo
            conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
            conn.commit()
            print("✅ Tabla alembic_version eliminada con éxito de la nube.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    limpiar()