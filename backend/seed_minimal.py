"""Minimal production seed for Render deployments.

Creates only the base roles and a superadmin account when they do not exist.
It is intentionally small so deploys do not fill production with demo data.
"""

import os

import app.db.base  # noqa: F401 - registers SQLAlchemy relationships before querying
from app.core.security import obtener_hash_clave
from app.db.session import SessionLocal
from app.models.rol import Rol
from app.models.usuario import Usuario


ROLES_BASE = [
    {"id": 1, "nombre": "Administrador de Taller"},
    {"id": 2, "nombre": "Cliente"},
    {"id": 3, "nombre": "Técnico"},
    {"id": 4, "nombre": "Super Administrador"},
]


def seed_minimal() -> None:
    db = SessionLocal()
    try:
        for rol in ROLES_BASE:
            if not db.query(Rol).filter(Rol.id == rol["id"]).first():
                db.add(Rol(**rol))
        db.commit()

        email = os.getenv("SUPERADMIN_EMAIL", "admin@super.com")
        password = os.getenv("SUPERADMIN_PASSWORD", "password123")

        if not db.query(Usuario).filter(Usuario.correo == email).first():
            db.add(
                Usuario(
                    nombre="Super Administrador",
                    correo=email,
                    clave_hash=obtener_hash_clave(password),
                    rol_id=4,
                    taller_id=None,
                    esta_activo=True,
                    telefono=os.getenv("SUPERADMIN_PHONE", "77777777"),
                )
            )
            db.commit()
            print(f"Superadmin creado: {email}")
        else:
            print(f"Superadmin existente: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_minimal()
