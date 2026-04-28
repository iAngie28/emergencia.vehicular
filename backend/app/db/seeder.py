import logging
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from decimal import Decimal
from app.db.session import SessionLocal
from faker import Faker
import random

# Funcion auxiliar para convertir string a time
def parse_time(time_str: str) -> time:
    """Convierte string 'HH:MM' a objeto time de Python"""
    return datetime.strptime(time_str, "%H:%M").time()

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

# Inicializar Faker
fake = Faker('es_ES')
Faker.seed(42)  # Para reproducibilidad

# =================================================================
# 📍 COORDENADAS GPS DE SANTA CRUZ DE LA SIERRA, BOLIVIA
# =================================================================
# Centro de SC: -17.7869, -63.1904
# Rango aproximado: -17.65 a -17.85 lat, -63.05 a -63.35 lon

ZONAS_SC = [
    {"nombre": "Centro (Av. Banzer)", "lat": -17.786, "lon": -63.190, "radio": 0.02},
    {"nombre": "Plan 3000", "lat": -17.832, "lon": -63.135, "radio": 0.025},
    {"nombre": "Equipetrol", "lat": -17.761, "lon": -63.195, "radio": 0.02},
    {"nombre": "Villa 1ro de Mayo", "lat": -17.815, "lon": -63.182, "radio": 0.015},
    {"nombre": "Av. Santos Dumont", "lat": -17.795, "lon": -63.128, "radio": 0.015},
    {"nombre": "La Guardia Km 9", "lat": -17.865, "lon": -63.245, "radio": 0.03},
    {"nombre": "8vo Anillo Norte", "lat": -17.712, "lon": -63.158, "radio": 0.02},
    {"nombre": "Doble Vía La Guardia", "lat": -17.808, "lon": -63.208, "radio": 0.025},
]

CLASIFICACIONES_INCIDENTES = [
    "Falla de Motor",
    "Mantenimiento Preventivo",
    "Alineación y Balanceo",
    "Sistema de Frenos",
    "Fuga de refrigerante",
    "Aire Acondicionado",
    "Escaneo Computarizado",
    "Bomba de Gasolina",
    "Falla Eléctrica",
    "Revisión de Batería",
    "Sobrecalentamiento",
    "Falla de Embrague",
    "Ruido en Suspensión",
    "Pinchazo",
    "Cambio de Aceite",
    "Pastillas de Freno",
    "Filtro de Aire",
    "Correa de Distribución",
    "Radiador",
    "Bujías",
]

ESPECIALIDADES_NOMBRE = [
    "Mecánica General",
    "Electricidad Automotriz",
    "Llantería",
    "Refrigeración",
    "Transmisiones",
]

def generar_coords_en_zona(zona):
    """Genera coordenadas GPS dentro de una zona de SC"""
    lat = zona["lat"] + random.uniform(-zona["radio"], zona["radio"])
    lon = zona["lon"] + random.uniform(-zona["radio"], zona["radio"])
    return Decimal(str(round(lat, 6))), Decimal(str(round(lon, 6)))


def seed_db(db: Session) -> None:
    logger.info("[INIT] Iniciando sembrado avanzado con FAKER (ultimos 365 dias - 1 ano)...")
    
    hash_clave = get_password_hash("password123")
    hoy = datetime.now()
    
    # ---------------------------------------------------------
    # 1. ROLES
    # ---------------------------------------------------------
    logger.info("[ROLES] Creando ROLES...")
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
    logger.info("[SPECIALTIES] Creando ESPECIALIDADES...")
    especialidades = []
    for idx, nombre in enumerate(ESPECIALIDADES_NOMBRE, start=1):
        esp = db.query(Especialidad).filter(Especialidad.id == idx).first()
        if not esp:
            esp = Especialidad(id=idx, nombre=nombre, descripcion=f"Especialista en {nombre}")
            db.add(esp)
            especialidades.append(esp)
        else:
            especialidades.append(esp)
    db.commit()
    
    # ---------------------------------------------------------
    # 3. TALLERES (6 talleres en SC)
    # ---------------------------------------------------------
    logger.info("[SHOPS] Creando TALLERES en Santa Cruz...")
    talleres_data = [
        {
            "nombre": "Taller Central SC",
            "direccion": "Av. Banzer 4to Anillo",
            "comision": 10.0,
            "zona": ZONAS_SC[0]
        },
        {
            "nombre": "Super Mecánica Plan 3000",
            "direccion": "Av. 4 Esquina 3er Anillo",
            "comision": 12.0,
            "zona": ZONAS_SC[1]
        },
        {
            "nombre": "Talleres Equipetrol",
            "direccion": "Av. Equipetrol",
            "comision": 11.0,
            "zona": ZONAS_SC[2]
        },
        {
            "nombre": "Mecánica Villa 1ro",
            "direccion": "Villa 1ro de Mayo",
            "comision": 9.5,
            "zona": ZONAS_SC[3]
        },
        {
            "nombre": "Auto Servicio Santos",
            "direccion": "Av. Santos Dumont 3er Anillo",
            "comision": 13.0,
            "zona": ZONAS_SC[4]
        },
        {
            "nombre": "Taller Express La Guardia",
            "direccion": "La Guardia Km 9",
            "comision": 10.5,
            "zona": ZONAS_SC[5]
        },
    ]
    
    talleres = []
    for idx, t_data in enumerate(talleres_data, start=1):
        taller = db.query(Taller).filter(Taller.id == idx).first()
        if not taller:
            lat, lon = generar_coords_en_zona(t_data["zona"])
            taller = Taller(
                id=idx,
                nombre=t_data["nombre"],
                direccion=t_data["direccion"],
                comision_porcentaje=t_data["comision"],
                latitud=lat,
                longitud=lon,
                estado=True
            )
            db.add(taller)
            talleres.append(taller)
        else:
            talleres.append(taller)
            # Guardar zona en objeto para usarlo después
            taller.zona = t_data["zona"]
    db.commit()
    
    # ---------------------------------------------------------
    # 4. USUARIOS (Admins de taller, Técnicos, Clientes)
    # ---------------------------------------------------------
    logger.info("[USERS] Creando USUARIOS (Admins, Tecnicos, Clientes)...")
    usuario_id_counter = 1
    usuarios = []
    tecnicos = []
    clientes = []
    
    # Admins de taller (1 por taller)
    for idx, taller in enumerate(talleres, start=1):
        usuario = db.query(Usuario).filter(Usuario.correo == f"admin{idx}@taller.com").first()
        if not usuario:
            usuario = Usuario(
                id=usuario_id_counter,
                nombre=f"Admin {taller.nombre}",
                correo=f"admin{idx}@taller.com",
                clave_hash=hash_clave,
                rol_id=1,  # Admin
                taller_id=idx,
                esta_activo=True,
                telefono=fake.phone_number()[:20]  # Teléfono
            )
            db.add(usuario)
            usuarios.append(usuario)
            usuario_id_counter += 1
    db.commit()
    
    # Técnicos por taller (2-3 por taller)
    for taller in talleres:
        num_tecnicos = random.randint(2, 3)
        for t_idx in range(num_tecnicos):
            usuario = db.query(Usuario).filter(
                Usuario.correo == f"tec_{taller.id}_{t_idx}@taller.com"
            ).first()
            if not usuario:
                usuario = Usuario(
                    id=usuario_id_counter,
                    nombre=f"{fake.first_name()} {fake.last_name()}",
                    correo=f"tec_{taller.id}_{t_idx}@taller.com",
                    clave_hash=hash_clave,
                    rol_id=3,  # Técnico
                    taller_id=taller.id,
                    esta_activo=True,
                    telefono=fake.phone_number()[:20]  # Teléfono
                )
                # Asignar especialidades aleatorias
                esp = random.sample(especialidades, k=random.randint(1, 2))
                usuario.especialidades = esp
                db.add(usuario)
                usuarios.append(usuario)
                tecnicos.append(usuario)
                usuario_id_counter += 1
    db.commit()
    
    # Clientes (12-15 clientes que no tienen taller)
    for c_idx in range(12):
        usuario = db.query(Usuario).filter(
            Usuario.correo == f"cliente_{c_idx}@correo.com"
        ).first()
        if not usuario:
            usuario = Usuario(
                id=usuario_id_counter,
                nombre=fake.name(),
                correo=f"cliente_{c_idx}@correo.com",
                clave_hash=hash_clave,
                rol_id=2,  # Cliente
                taller_id=None,  # Sin taller
                esta_activo=True,
                telefono=fake.phone_number()[:20]  # Teléfono
            )
            db.add(usuario)
            usuarios.append(usuario)
            clientes.append(usuario)
            usuario_id_counter += 1
    db.commit()
    
    logger.info(f"[OK] Creados {len(usuarios)} usuarios")
    
    # ---------------------------------------------------------
    # 5. VEHÍCULOS (2-3 por cliente)
    # ---------------------------------------------------------
    logger.info("[VEHICLES] Creando VEHICULOS...")
    vehiculos = []
    marcas = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia", "BMW", "Mercedes"]
    modelos = ["Corolla", "Civic", "Focus", "Spark", "Versa", "Elantra", "Picanto", "320i", "C200"]
    
    for cliente in clientes:
        num_vehiculos = random.randint(1, 2)
        for v_idx in range(num_vehiculos):
            placa = f"{random.randint(1000, 9999)}-{fake.bothify('???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()
            if not vehiculo:
                vehiculo = Vehiculo(
                    placa=placa,
                    marca=random.choice(marcas),
                    modelo=random.choice(modelos),
                    usuario_id=cliente.id
                )
                db.add(vehiculo)
                vehiculos.append(vehiculo)
    db.commit()
    logger.info(f"[OK] Creados {len(vehiculos)} vehiculos")
    
    # ---------------------------------------------------------
    # 6. HORARIOS DE TALLERES
    # ---------------------------------------------------------
    logger.info("[SCHEDULES] Creando HORARIOS...")
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for taller in talleres:
        for dia in dias_semana:
            horario = db.query(HorarioTaller).filter(
                HorarioTaller.taller_id == taller.id,
                HorarioTaller.dia == dia
            ).first()
            if not horario:
                if dia == "domingo":
                    continue  # Cerrado el domingo
                elif dia == "sábado":
                    horario = HorarioTaller(
                        taller_id=taller.id,
                        dia=dia,
                        hora_apertura=parse_time("09:00"),
                        hora_cierre=parse_time("14:00")
                    )
                else:
                    horario = HorarioTaller(
                        taller_id=taller.id,
                        dia=dia,
                        hora_apertura=parse_time("08:00"),
                        hora_cierre=parse_time("18:00")
                    )
                db.add(horario)
    db.commit()
    logger.info("[OK] Horarios de talleres creados.")
    
    # ---------------------------------------------------------
    # 7. INCIDENTES (200-300 incidentes en 1 año)
    # ---------------------------------------------------------
    logger.info("[INCIDENTS] Creando INCIDENTES (ultimos 365 dias - 1 ANO)...")
    incidentes = []
    estados_incidente = ["pendiente", "en_proceso", "atendido", "cancelado"]
    prioridades = ["baja", "media", "alta"]
    
    # Calcular cuántos de cada estado
    num_incidentes = random.randint(250, 350)  # 250-350 incidentes en 1 año
    num_en_proceso = 20  # Solo 20 en proceso
    
    # Crear primero los 20 en_proceso
    incidentes_en_proceso = 0
    
    for inc_idx in range(num_incidentes):
        # Fecha aleatoria en los últimos 365 días (1 año)
        dias_atras = random.randint(0, 365)
        fecha_incidente = hoy - timedelta(days=dias_atras)
        
        # Seleccionar cliente y vehículo aleatorio
        cliente = random.choice(clientes)
        vehiculos_cliente = db.query(Vehiculo).filter(Vehiculo.usuario_id == cliente.id).all()
        if not vehiculos_cliente:
            continue
        vehiculo = random.choice(vehiculos_cliente)
        
        # Taller aleatorio
        taller = random.choice(talleres)
        
        # Distribución de estados: 20 en_proceso, resto distribuidos
        if incidentes_en_proceso < num_en_proceso:
            estado = "en_proceso"
            incidentes_en_proceso += 1
        else:
            estado = random.choices(estados_incidente, weights=[25, 0, 50, 25])[0]
        
        tecnico = None
        if estado in ["en_proceso", "atendido"]:
            tecnicos_taller = [t for t in tecnicos if t.taller_id == taller.id]
            if tecnicos_taller:
                tecnico = random.choice(tecnicos_taller)
        
        # Coordenadas en zona del taller o cercana
        zona = taller.zona if hasattr(taller, 'zona') else random.choice(ZONAS_SC)
        lat, lon = generar_coords_en_zona(zona)
        
        # Monto aleatorio
        monto = random.randint(150, 1500) if estado != "pendiente" else 0
        
        incidente = Incidente(
            vehiculo_id=vehiculo.id,
            usuario_id=cliente.id,
            taller_id=taller.id if estado != "pendiente" else None,
            tecnico_id=tecnico.id if tecnico else None,
            latitud=lat,
            longitud=lon,
            prioridad=random.choice(prioridades),
            estado=estado,
            pago_estado="pagado" if estado == "atendido" else "pendiente",
            clasificacion_ia=random.choice(CLASIFICACIONES_INCIDENTES),
            resumen_ia=fake.sentence(nb_words=8),
            fecha_creacion=fecha_incidente
        )
        db.add(incidente)
        incidentes.append(incidente)
    
    db.commit()
    logger.info(f"[OK] Creados {len(incidentes)} incidentes (20 en_proceso)")
    
    # ---------------------------------------------------------
    # 8. PAGOS (para incidentes atendidos)
    # ---------------------------------------------------------
    logger.info("[PAYMENTS] Creando PAGOS...")
    pagos = []
    for incidente in incidentes:
        if incidente.estado == "atendido" and incidente.taller_id:
            taller = db.query(Taller).get(incidente.taller_id)
            monto = Decimal(str(random.randint(150, 1500)))
            comision = monto * Decimal(str(taller.comision_porcentaje / 100.0))
            
            pago = Pago(
                incidente_id=incidente.id,
                usuario_id=incidente.usuario_id,
                taller_id=incidente.taller_id,
                monto=monto,
                comision_plataforma=comision,
                metodo_pago=random.choice(["qr", "efectivo", "tarjeta"]),
                estado=random.choice(["completado", "pendiente"]),
                fecha=incidente.fecha_creacion + timedelta(days=random.randint(1, 5))
            )
            db.add(pago)
            pagos.append(pago)
    
    db.commit()
    logger.info(f"[OK] Creados {len(pagos)} pagos")
    
    # ---------------------------------------------------------
    # 9. BITÁCORA (registros de actividades)
    # ---------------------------------------------------------
    logger.info("[AUDIT] Creando BITACORA...")
    bitacoras = []
    acciones = ["crear", "editar", "atender", "cancelar", "aprobar", "rechazar"]
    
    for incidente in incidentes[:100]:  # 100 registros de bitácora (más incidentes = más bitácoras)
        for _ in range(random.randint(1, 3)):
            bitacora = Bitacora(
                usuario_id=incidente.tecnico_id or incidente.usuario_id,
                taller_id=incidente.taller_id,
                tabla="incidente",
                tabla_id=incidente.id,
                accion=random.choice(acciones),
                valor_anterior={"estado": "pendiente"},
                valor_nuevo={"estado": incidente.estado},
                fecha_hora=incidente.fecha_creacion + timedelta(hours=random.randint(1, 72))
            )
            db.add(bitacora)
            bitacoras.append(bitacora)
    
    db.commit()
    logger.info(f"[OK] Creados {len(bitacoras)} registros de bitacora")
    
    # ---------------------------------------------------------
    # 10. EVIDENCIAS (fotos de incidentes)
    # ---------------------------------------------------------
    logger.info("[EVIDENCE] Creando EVIDENCIAS...")
    evidencias = []
    
    for incidente in incidentes[:80]:  # 80 incidentes con evidencia (más con 1 año de datos)
        if incidente.estado in ["en_proceso", "atendido"]:
            num_fotos = random.randint(1, 3)
            for foto_idx in range(num_fotos):
                evidencia = Evidencia(
                    incidente_id=incidente.id,
                    tipo_archivo="imagen",
                    url_archivo=f"https://placeholder.com/300?text=Evidencia+{foto_idx+1}",
                    fecha_registro=incidente.fecha_creacion + timedelta(hours=random.randint(2, 48))
                )
                db.add(evidencia)
                evidencias.append(evidencia)
    
    db.commit()
    logger.info(f"[OK] Creados {len(evidencias)} registros de evidencia")
    
    # ---------------------------------------------------------
    # 11. NOTIFICACIONES (para incidentes cercanos)
    # ---------------------------------------------------------
    logger.info("[NOTIFICATIONS] Creando NOTIFICACIONES...")
    notificaciones = []
    
    for incidente in incidentes[:60]:  # 60 notificaciones (más con 1 año)
        if incidente.taller_id:
            notificacion = Notificacion(
                usuario_id=incidente.usuario_id,
                incidente_id=incidente.id,
                titulo="Incidente cercano reportado",
                mensaje=f"Se reportó un {incidente.clasificacion_ia} cerca de tu ubicación",
                tipo="incidente_cercano",
                leido=random.choice([True, False]),
                fecha_envio=incidente.fecha_creacion
            )
            db.add(notificacion)
            notificaciones.append(notificacion)
    
    db.commit()
    logger.info(f"[OK] Creados {len(notificaciones)} registros de notificacion")
    
    # ---------------------------------------------------------
    # RESUMEN FINAL
    # ---------------------------------------------------------
    logger.info("\n" + "="*70)
    logger.info("[SUCCESS] SEMBRADO COMPLETADO EXITOSAMENTE")
    logger.info("="*70)
    logger.info(f"[ROLES] Roles: {db.query(Rol).count()}")
    logger.info(f"[SPECIALTIES] Especialidades: {db.query(Especialidad).count()}")
    logger.info(f"[SHOPS] Talleres: {db.query(Taller).count()}")
    logger.info(f"[USERS] Usuarios: {db.query(Usuario).count()}")
    logger.info(f"[VEHICLES] Vehiculos: {db.query(Vehiculo).count()}")
    logger.info(f"[SCHEDULES] Horarios: {db.query(HorarioTaller).count()}")
    logger.info(f"[INCIDENTS] Incidentes: {db.query(Incidente).count()}")
    logger.info(f"[PAYMENTS] Pagos: {db.query(Pago).count()}")
    logger.info(f"[AUDIT] Bitacora: {db.query(Bitacora).count()}")
    logger.info(f"[EVIDENCE] Evidencias: {db.query(Evidencia).count()}")
    logger.info(f"[NOTIFICATIONS] Notificaciones: {db.query(Notificacion).count()}")
    logger.info("="*70)
    logger.info("[DATA] Datos de 1 ANO COMPLETO de movimiento en Santa Cruz de la Sierra")
    logger.info("="*70 + "\n")



if __name__ == "__main__":
    # Permite ejecutar `python seeder.py` directamente
    db = SessionLocal()
    try:
        seed_db(db)
        print("[OK] Seeder ejecutado con exito!")
    except Exception as e:
        print(f"[ERROR] Error al ejecutar el seeder: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()