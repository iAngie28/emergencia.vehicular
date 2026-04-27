import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from decimal import Decimal
from app.db.session import SessionLocal

# =================================================================
# 🚩 BLOQUE DE IMPORTACIONES DE SEGURIDAD (No tocar)
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
    logger.info("🌱 Iniciando el sembrado de base de datos (Seeder)...")
    hash_clave = get_password_hash("password123")
    hoy = datetime.now()

    # ---------------------------------------------------------
    # 1. ROLES
    # ---------------------------------------------------------
    roles_base = [
        {"id": 1, "nombre": "Administrador de Taller"},
        {"id": 2, "nombre": "Cliente"},
        {"id": 3, "nombre": "Técnico"}
    ]
    for r in roles_base:
        if not db.query(Rol).filter(Rol.id == r["id"]).first():
            db.add(Rol(**r))
    db.commit()

    # ---------------------------------------------------------
    # 2. ESPECIALIDADES
    # ---------------------------------------------------------
    especialidades = [
        {"id": 1, "nombre": "Mecánica General", "descripcion": "Reparación de motores y transmisión"},
        {"id": 2, "nombre": "Electricidad Automotriz", "descripcion": "Baterías, alternadores, cableado"},
        {"id": 3, "nombre": "Llantería", "descripcion": "Cambio y parchado de llantas"}
    ]
    for e in especialidades:
        if not db.query(Especialidad).filter(Especialidad.id == e["id"]).first():
            db.add(Especialidad(**e))
    db.commit()

    # ---------------------------------------------------------
    # 3. TALLERES (Multi-Tenant) con UBICACIONES GPS
    # ---------------------------------------------------------
    talleres = [
        # Taller Central: Av. Banzer 4to Anillo, Santa Cruz
        {"id": 1, "nombre": "Taller Central Santa Cruz", "direccion": "Av. Banzer 4to Anillo", 
         "comision_porcentaje": 10.0, "latitud": -17.78, "longitud": -63.18},
        # Taller Warnes: Zona norte, hacia Warnes
        {"id": 2, "nombre": "Súper Mecánica Warnes", "direccion": "Ruta al Norte Km 20", 
         "comision_porcentaje": 15.0, "latitud": -17.82, "longitud": -63.22}
    ]
    for t in talleres:
        if not db.query(Taller).filter(Taller.id == t["id"]).first():
            db.add(Taller(**t))
    db.commit()

    # ---------------------------------------------------------
    # 4. USUARIOS (Admins, Clientes y Técnicos)
    # ---------------------------------------------------------
    usuarios = [
        # Admins de Taller
        {"id": 1, "nombre": "Admin Central", "correo": "admin1@taller.com", "clave_hash": hash_clave, "rol_id": 1, "taller_id": 1},
        {"id": 2, "nombre": "Admin Warnes", "correo": "admin2@taller.com", "clave_hash": hash_clave, "rol_id": 1, "taller_id": 2},
        # Cliente
        {"id": 3, "nombre": "Carlos Cliente", "correo": "carlos@cliente.com", "clave_hash": hash_clave, "rol_id": 2},
        # Técnicos Taller 1
        {"id": 4, "nombre": "Juan Mecánico", "correo": "tec1@taller.com", "clave_hash": hash_clave, "rol_id": 3, "taller_id": 1, "esta_activo": True},
        {"id": 5, "nombre": "Pedro Eléctrico", "correo": "tec2@taller.com", "clave_hash": hash_clave, "rol_id": 3, "taller_id": 1, "esta_activo": True},
        # Técnico Taller 2
        {"id": 6, "nombre": "Roberto Llantas", "correo": "tec3@taller.com", "clave_hash": hash_clave, "rol_id": 3, "taller_id": 2, "esta_activo": True},
    ]
    for u in usuarios:
        if not db.query(Usuario).filter(Usuario.correo == u["correo"]).first():
            db.add(Usuario(**u))
    db.commit()

    # Asignar especialidades a técnicos
    tec1 = db.query(Usuario).get(4) # Juan
    esp1 = db.query(Especialidad).get(1)
    if tec1 and esp1 and esp1 not in tec1.especialidades: tec1.especialidades.append(esp1)

    tec2 = db.query(Usuario).get(5) # Pedro
    esp2 = db.query(Especialidad).get(2)
    if tec2 and esp2 and esp2 not in tec2.especialidades: tec2.especialidades.append(esp2)
    db.commit()

    # ---------------------------------------------------------
    # 5. VEHÍCULO
    # ---------------------------------------------------------
    if not db.query(Vehiculo).filter(Vehiculo.placa == "1234-ABC").first():
        db.add(Vehiculo(id=1, placa="1234-ABC", marca="Toyota", modelo="Corolla", usuario_id=3))
    db.commit()

    # ---------------------------------------------------------
    # 6. INCIDENTES Y PAGOS (Generación de Historial y Métricas)
    # ---------------------------------------------------------
    # Tupla: (taller_id, tecnico_id, dias_atras, clasificacion, monto, estado, latitud, longitud)
    # 📍 Coordenadas GPS en Santa Cruz de la Sierra, Bolivia
    # Taller 1: -17.78, -63.18 (Centro - Av. Banzer)
    # Taller 2: -17.82, -63.22 (Warnes)
    datos_historial = [
        # Taller 1 - Historial (Atendidos) con distancias variadas
        (1, 4, 15, "Falla de Motor", 850, "atendido", -17.75, -63.18),      # 📍 Muy cerca (3.3 km)
        (1, 4, 8, "Mantenimiento", 300, "atendido", -17.80, -63.15),        # 📍 Cerca (3.7 km)
        (1, 5, 5, "Problema Batería", 450, "atendido", -17.82, -63.22),     # 📍 Lejos (4.8 km)
        (1, 5, 2, "Falla Eléctrica", 600, "atendido", -17.70, -63.10),      # 📍 Muy lejos (11 km)
        (1, 4, 1, "Cancelado por cliente", 0, "cancelado", -17.77, -63.19), # 📍 Cancelado (1.1 km)
        # Taller 1 - Activos (Disponibles y En proceso)
        (1, None, 0, "Falla Eléctrica (Pendiente)", 0, "pendiente", -17.76, -63.17),     # 📍 Sin asignar (2.2 km)
        (1, 5, 0, "Falla en Transmisión", 0, "en_proceso", -17.79, -63.20),  # 📍 En curso (2.2 km)
        
        # Taller 2 - Historial (No debe verse en Taller 1)
        (2, 6, 3, "Llanta pinchada", 150, "atendido", -17.85, -63.25),      # 📍 Taller 2 (4.2 km)
    ]

    # Contar si ya hay incidentes para no duplicar si corres el seeder varias veces
    if db.query(Incidente).count() < len(datos_historial):
        for idx, (taller_id, tec_id, dias, clase, monto, estado, lat, lon) in enumerate(datos_historial, start=1):
            fecha = hoy - timedelta(days=dias)
            
            # Si está cancelado o en proceso, el pago_estado es diferente
            pago_estado = "pagado" if estado == "atendido" else "pendiente"

            inc = Incidente(
                id=idx,
                vehiculo_id=1,
                usuario_id=3,
                taller_id=taller_id,
                tecnico_id=tec_id if estado != "pendiente" else None,
                latitud=lat,
                longitud=lon,
                prioridad="alta" if dias >= 5 else ("media" if dias >= 2 else "baja"),
                estado=estado, 
                pago_estado=pago_estado,
                clasificacion_ia=clase,
                resumen_ia=f"Problema detectado hace {dias} días",
                fecha_creacion=fecha
            )
            db.merge(inc)
            db.commit()

            # Generar pago solo para los atendidos (impacta en métricas financieras)
            if estado == "atendido":
                comision = Decimal(str(monto)) * Decimal(str(talleres[taller_id-1]["comision_porcentaje"] / 100.0))
                pago = Pago(
                    incidente_id=inc.id,
                    usuario_id=3,
                    taller_id=taller_id,
                    monto=Decimal(str(monto)),
                    comision_plataforma=comision,
                    metodo_pago="qr",
                    estado="completado",
                    fecha=fecha
                )
                db.merge(pago)
        
        db.commit()
        logger.info("✅ Incidentes y Pagos de historial creados exitosamente.")
        logger.info("📍 Incluye incidentes con UBICACIONES GPS variadas para pruebas de distancia.")

if __name__ == "__main__":
    # Permite ejecutar `python seeder.py` directamente
    db = SessionLocal()
    try:
        seed_db(db)
        print("🎉 ¡Seeder ejecutado con éxito!")
    except Exception as e:
        print(f"❌ Error al ejecutar el seeder: {e}")
        db.rollback()
    finally:
        db.close()