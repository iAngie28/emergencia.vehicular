import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

# =================================================================
# 🚩 BLOQUE DE IMPORTACIONES DE SEGURIDAD (No tocar)
# Importamos todos los modelos para que SQLAlchemy registre las relaciones
# =================================================================
from app.models.rol import Rol
from app.models.taller import Taller
from app.models.usuario import Usuario, Especialidad
from app.models.vehiculo import Vehiculo   
from app.models.incidente import Incidente 
from app.models.pago import Pago 
from app.models.bitacora import Bitacora
from app.models.notificacion import Notificacion
from app.models.evidencia import Evidencia
from app.models.taller_detalle import HorarioTaller


from app.core.security import obtener_hash_clave as get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_db(db: Session) -> None:
    # 1. ROLES
    roles_base = [
        {"id": 1, "nombre": "Administrador de Taller"},
        {"id": 2, "nombre": "Cliente"},
        {"id": 3, "nombre": "Técnico"}
    ]
    for r in roles_base:
        if not db.query(Rol).filter(Rol.id == r["id"]).first():
            db.add(Rol(**r))
    db.commit()

    # 2. ESPECIALIDADES
    especialidades_base = [
        {"id": 1, "nombre": "Mecánica General"},
        {"id": 2, "nombre": "Electromecánica"},
        {"id": 3, "nombre": "Chapería y Pintura"},
        {"id": 4, "nombre": "Frenos"}
    ]
    for e in especialidades_base:
        if not db.query(Especialidad).filter(Especialidad.id == e["id"]).first():
            db.add(Especialidad(**e))
    db.commit()

    # 3. TALLERES
    if not db.query(Taller).filter(Taller.id == 1).first():
        db.add(Taller(
            id=1, nombre="Mecánica Central 2do Anillo", 
            latitud=-17.7761, longitud=-63.1782, estado=True,
            direccion="Av. Cristóbal de Mendoza", telefono="70011111"
        ))
    db.commit()

    # 4. USUARIOS
    hash_clave = get_password_hash("pas12345")
    usuarios = [
        {"id": 1, "nombre": "Admin T1", "correo": "adm1@taller.com", "clave_hash": hash_clave, "rol_id": 1, "taller_id": 1},
        {"id": 2, "nombre": "Carlos Cliente", "correo": "carlos@cliente.com", "clave_hash": hash_clave, "rol_id": 2},
        {"id": 3, "nombre": "Juan Mecánico", "correo": "tec1@taller.com", "clave_hash": hash_clave, "rol_id": 3, "taller_id": 1, "esta_activo": True},
    ]

    for u in usuarios:
        if not db.query(Usuario).filter(Usuario.correo == u["correo"]).first():
            db.add(Usuario(**u))
    db.commit()

    # Vincular Especialidad al técnico
    tec = db.query(Usuario).get(3)
    esp = db.query(Especialidad).get(1)
    if tec and esp and esp not in tec.especialidades:
        tec.especialidades.append(esp)
    db.commit()

    # 5. VEHÍCULO
    if not db.query(Vehiculo).filter(Vehiculo.placa == "1234-ABC").first():
        db.add(Vehiculo(id=1, placa="1234-ABC", marca="Toyota", modelo="Corolla", usuario_id=2))
    db.commit()

    # 6. INCIDENTE
    if not db.query(Incidente).filter(Incidente.id == 1).first():
        db.add(Incidente(
            id=1, vehiculo_id=1, usuario_id=2, 
            latitud=-17.7833, longitud=-63.1821, prioridad="alta", 
            estado="pendiente", transcripcion_audio="Ruido en el motor",
            clasificacion_ia="Mecánica", resumen_ia="Falla en motor"
        ))
    db.commit()
    logger.info("🚀 Seeder finalizado con éxito.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()