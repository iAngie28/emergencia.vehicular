#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script mejorado para resetear la base de datos sin problemas de encoding
"""
import os
import sys
import subprocess

# CONFIGURAR ENCODING
os.environ['PYTHONIOENCODING'] = 'utf-8'
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Agregar ruta del módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("[INIT] Iniciando reset de BD...")

# Cargar variables de entorno
from dotenv import load_dotenv
if os.path.exists(".env"):
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
is_postgres = DATABASE_URL.startswith("postgresql")

print(f"[INFO] DATABASE_URL: {DATABASE_URL[:50]}...")
print(f"[INFO] Tipo: {'PostgreSQL' if is_postgres else 'SQLite'}")

try:
    # Importar después de cargar .env
    from app.db.base import Base
    from app.db.session import SessionLocal, engine
    from app.db.seeder import seed_db
    from sqlalchemy import text
    
    print("[BUILD] Creando tablas desde modelos...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Tablas creadas")
    
    print("[SEED] Poblando base de datos...")
    db = SessionLocal()
    try:
        seed_db(db)
        print("[OK] Datos insertados")
    finally:
        db.close()
    
    # Alembic stamp
    print("[STAMP] Marcando versión en Alembic...")
    result = subprocess.run(
        "alembic stamp head",
        shell=True,
        capture_output=True,
        encoding='utf-8',
        errors='replace'
    )
    if result.returncode == 0:
        print("[OK] Alembic stamp completado")
    else:
        print("[WARN] Alembic stamp falló (continuando)")
    
    print("\n[SUCCESS] BASE DE DATOS INICIALIZADA!")
    
except Exception as e:
    error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
    print(f"[ERROR] {error_msg[:200]}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
