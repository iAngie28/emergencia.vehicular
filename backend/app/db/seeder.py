import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.base import Base
from app.models.rol import Rol
from app.models.taller import Taller
from app.models.usuario import Usuario
from app.models.vehiculo import Vehiculo   # 👈 Agregado
from app.models.incidente import Incidente # 👈 Agregado
# Asegúrate de importar tu función para encriptar contraseñas. 
from app.core.security import obtener_hash_clave as get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_db(db: Session) -> None:
    # ==========================================
    # 1. CREAR ROLES (Si no existen)
    # ==========================================
    roles_base = [
        {"id": 1, "nombre": "Administrador de Taller"},
        {"id": 2, "nombre": "Cliente"}
    ]
    
    for r in roles_base:
        rol = db.query(Rol).filter(Rol.id == r["id"]).first()
        if not rol:
            nuevo_rol = Rol(id=r["id"], nombre=r["nombre"])
            db.add(nuevo_rol)
    db.commit()
    logger.info("✅ Roles verificados/creados.")

    # ==========================================
    # 2. CREAR TALLERES BASE
    # ==========================================
    talleres_base = [
        {
            "id": 1, 
            "nombre": "Mecánica Central 2do Anillo", 
            "direccion": "Av. Cristóbal de Mendoza", 
            "latitud": -17.7761, 
            "longitud": -63.1782, 
            "comision_porcentaje": 10.0
        },
        {
            "id": 2, 
            "nombre": "AutoServicio Equipetrol", 
            "direccion": "Av. San Martín", 
            "latitud": -17.7654, 
            "longitud": -63.1956, 
            "comision_porcentaje": 12.5
        }
    ]

    for t in talleres_base:
        taller = db.query(Taller).filter(Taller.id == t["id"]).first()
        if not taller:
            nuevo_taller = Taller(**t)
            db.add(nuevo_taller)
    db.commit()
    logger.info("✅ Talleres verificados/creados.")

    # ==========================================
    # 3. CREAR USUARIOS (Admins y Clientes)
    # ==========================================
    clave_generica = get_password_hash("pas12345") # Contraseña estándar para pruebas

    usuarios_base = [
        # Administradores del Taller 1 (Tienen rol_id=1 y taller_id=1)
        {"nombre": "Admin Taller 1A", "correo": "adm1a@taller.com", "clave_hash": clave_generica, "rol_id": 1, "taller_id": 1},
        {"nombre": "Admin Taller 1B", "correo": "adm1b@taller.com", "clave_hash": clave_generica, "rol_id": 1, "taller_id": 1},
        
        # Administradores del Taller 2 (Tienen rol_id=1 y taller_id=2)
        {"nombre": "Admin Taller 2A", "correo": "adm2a@taller.com", "clave_hash": clave_generica, "rol_id": 1, "taller_id": 2},
        {"nombre": "Admin Taller 2B", "correo": "adm2b@taller.com", "clave_hash": clave_generica, "rol_id": 1, "taller_id": 2},
        
        # Clientes de la App (Tienen rol_id=2 y taller_id=None)
        {"nombre": "Carlos Cliente", "correo": "carlos@cliente.com", "clave_hash": clave_generica, "rol_id": 2, "taller_id": None},
        {"nombre": "Maria Cliente", "correo": "maria@cliente.com", "clave_hash": clave_generica, "rol_id": 2, "taller_id": None},
    ]

    for u in usuarios_base:
        usuario = db.query(Usuario).filter(Usuario.correo == u["correo"]).first()
        if not usuario:
            nuevo_usuario = Usuario(**u)
            db.add(nuevo_usuario)
    db.commit()
    logger.info("✅ Usuarios verificados/creados.")

    # ==========================================
    # 4. CREAR VEHÍCULOS PARA CLIENTES (NUEVO)
    # ==========================================
    carlos = db.query(Usuario).filter(Usuario.correo == "carlos@cliente.com").first()
    maria = db.query(Usuario).filter(Usuario.correo == "maria@cliente.com").first()

    vehiculos_base = [
        {"placa": "1234-ABC", "marca": "Toyota", "modelo": "Corolla", "anio": 2020, "color": "Blanco", "usuario_id": carlos.id},
        {"placa": "5678-XYZ", "marca": "Suzuki", "modelo": "Vitara", "anio": 2022, "color": "Azul", "usuario_id": maria.id}
    ]

    for v in vehiculos_base:
        vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == v["placa"]).first()
        if not vehiculo:
            nuevo_vehiculo = Vehiculo(**v)
            db.add(nuevo_vehiculo)
    db.commit()
    logger.info("✅ Vehículos de prueba creados.")

    # ==========================================
    # 5. CREAR INCIDENTES PENDIENTES (NUEVO)
    # ==========================================
    v_carlos = db.query(Vehiculo).filter(Vehiculo.usuario_id == carlos.id).first()
    v_maria = db.query(Vehiculo).filter(Vehiculo.usuario_id == maria.id).first()

    incidentes_base = [
        {
            "vehiculo_id": v_carlos.id, 
            "usuario_id": carlos.id,
            "latitud": -17.783312, 
            "longitud": -63.182123, 
            "prioridad": "alta", 
            "estado": "pendiente",
            "transcripcion_audio": "El motor está haciendo un ruido metálico fuerte y se apagó en medio de la avenida.",
            "clasificacion_ia": "Falla mecánica crítica", 
            "resumen_ia": "Posible rotura de correa o falla de motor interna. Requiere remolque inmediato."
        },
        {
            "vehiculo_id": v_maria.id, 
            "usuario_id": maria.id,
            "latitud": -17.771234, 
            "longitud": -63.192345, 
            "prioridad": "media", 
            "estado": "pendiente",
            "transcripcion_audio": "Tengo una llanta pinchada y no tengo la llave cruz para cambiarla.",
            "clasificacion_ia": "Auxilio de neumático", 
            "resumen_ia": "Cambio de llanta pinchada. El cliente no cuenta con herramientas."
        }
    ]

    for i in incidentes_base:
        # Evitamos duplicar incidentes pendientes para el mismo vehículo
        incidente = db.query(Incidente).filter(
            Incidente.vehiculo_id == i["vehiculo_id"], 
            Incidente.estado == "pendiente"
        ).first()
        if not incidente:
            nuevo_incidente = Incidente(**i)
            db.add(nuevo_incidente)
    db.commit()
    logger.info("✅ Incidentes de prueba creados.")
    
    logger.info("🎉 ¡Base de datos poblada con éxito! (Contraseña de todos: 'pas12345')")

if __name__ == "__main__":
    logger.info("Iniciando el seeder de base de datos...")
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()