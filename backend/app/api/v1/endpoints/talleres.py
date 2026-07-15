from datetime import date, datetime, time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional

from app.api import deps  # 👈 Aquí vive la magia de la seguridad
from app.crud.crud_taller import taller_crud
from app.crud.crud_bitacora import bitacora_crud
from app.schemas.taller import (
    Taller,
    TallerCreate,
    TallerUpdate,
    TallerDirectorioOut,
    TallerDetalleSuperadmin,
    TallerEmergenciaResumen,
    TallerReporteResumen,
    TallerTecnicoResumen,
)
from app.services.ranking_taller_service import RankingTallerService
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# 1. Registrar un nuevo taller (SaaS onboarding)
@router.post("/", response_model=Taller)
def registrar_taller(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: TallerCreate,
    # Usamos la dependencia que definimos en deps.py
    current_user = Depends(deps.get_current_active_user) 
):
    """Registra un taller y lo vincula al admin actual."""
    nuevo_taller = taller_crud.create(db, obj_in=obj_in)
    
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=nuevo_taller.id,
        tabla="talleres",
        tabla_id=nuevo_taller.id,
        accion="CREATE_TALLER",
        nuevo=obj_in.dict()
    )
    return nuevo_taller

# 2. Listar talleres activos (Para el mapa de la App Móvil)
@router.get("/activos", response_model=List[Taller])
def leer_talleres_activos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    return taller_crud.obtener_activos(db, skip=skip, limit=limit)

# 2.5. Directorio de Talleres (solo consulta): talleres activos por especialidad,
# ordenados por la lógica de ranking priorizando la mejor calificación promedio.
@router.get("/directorio", response_model=List[TallerDirectorioOut])
def directorio_talleres(
    especialidad_id: int,
    latitud: float | None = None,
    longitud: float | None = None,
    db: Session = Depends(deps.get_db),
):
    resultados = RankingTallerService(db).recomendar_talleres_por_especialidad(
        especialidad_id=especialidad_id,
        latitud=latitud,
        longitud=longitud,
    )

    tarjetas: List[TallerDirectorioOut] = []
    for item in resultados:
        taller = item["taller"]
        distancia_metros = item["distancia_metros"]
        tarjetas.append(
            TallerDirectorioOut(
                id=taller.id,
                nombre=taller.nombre,
                especialidad=item["especialidad"],
                direccion=taller.direccion,
                ciudad=taller.ciudad,
                telefono=taller.telefono,
                latitud=taller.latitud,
                longitud=taller.longitud,
                calificacion_promedio=taller.calificacion_promedio,
                especialidades_activas=taller.especialidades_activas,
                esta_abierto_ahora=taller.esta_abierto_ahora,
                distancia_km=round(distancia_metros / 1000, 1) if distancia_metros is not None else None,
            )
        )
    return tarjetas

# 3. MI TALLER: El perfil que el admin gestiona (Endpoint /me)
@router.get("/me", response_model=Taller)
def obtener_mi_taller(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    taller = taller_crud.get(db, id=current_user.taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return taller

# 3.5. Estado actual del taller (Abierto/Cerrado)
@router.get("/me/status", response_model=dict)
def obtener_status_taller(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Obtiene si el taller está abierto AHORA"""
    taller = taller_crud.get(db, id=current_user.taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    
    return {
        "taller_id": taller.id,
        "nombre": taller.nombre,
        "esta_abierto_ahora": taller.esta_abierto_ahora,
        "estado": "🟢 ABIERTO" if taller.esta_abierto_ahora else "🔴 CERRADO"
    }

@router.put("/me", response_model=Taller)
def actualizar_mi_taller(
    obj_in: TallerUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    taller_db = taller_crud.get(db, id=current_user.taller_id)
    if not taller_db:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    # 💾 Preparamos los datos para la Bitácora (limpios de Decimals)
    # jsonable_encoder asegura que latitud/longitud sean serializables
    anterior_contenido = jsonable_encoder(taller_db)
    
    # Realizamos la actualización en la DB
    taller_actualizado = taller_crud.update(db, db_obj=taller_db, obj_in=obj_in)
    
    # Obtenemos el contenido nuevo ya procesado
    nuevo_contenido = jsonable_encoder(taller_actualizado)

    # 📝 REGISTRO COMPLETO EN BITÁCORA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="talleres",
        tabla_id=taller_db.id,
        accion="UPDATE_PERFIL_TALLER",
        anterior=anterior_contenido, # 👈 ¡Faltaba pasar este!
        nuevo=nuevo_contenido
    )
    
    return taller_actualizado

@router.get("/", response_model=List[Taller])
def listar_todos_los_talleres(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_superadmin),
    nombre: Optional[str] = Query(None),
    ciudad: Optional[str] = Query(None),
    estado: Optional[bool] = Query(None),
    fecha_desde: Optional[date] = Query(None),
    fecha_hasta: Optional[date] = Query(None),
):
    """(Superadmin) Retorna los talleres registrados con filtros opcionales."""
    from app.models.taller import Taller as TallerModel

    query = db.query(TallerModel).options(selectinload(TallerModel.usuarios))

    if nombre:
        query = query.filter(TallerModel.nombre.ilike(f"%{nombre.strip()}%"))
    if ciudad:
        query = query.filter(TallerModel.ciudad.ilike(f"%{ciudad.strip()}%"))
    if estado is not None:
        query = query.filter(TallerModel.estado == estado)
    if fecha_desde:
        query = query.filter(TallerModel.fecha_creacion >= datetime.combine(fecha_desde, time.min))
    if fecha_hasta:
        query = query.filter(TallerModel.fecha_creacion <= datetime.combine(fecha_hasta, time.max))

    return query.order_by(TallerModel.fecha_creacion.desc(), TallerModel.id.desc()).all()


@router.get("/superadmin/{id}/detalle", response_model=TallerDetalleSuperadmin)
def obtener_detalle_taller_superadmin(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_superadmin),
):
    """(Superadmin) Consulta detalle completo de un taller sin impersonar."""
    from app.models.incidente import Incidente as IncidenteModel
    from app.models.reporte import Reporte as ReporteModel
    from app.models.taller import Taller as TallerModel
    from app.models.usuario import Usuario as UsuarioModel

    taller = (
        db.query(TallerModel)
        .options(
            selectinload(TallerModel.usuarios).selectinload(UsuarioModel.especialidades),
            selectinload(TallerModel.horarios),
        )
        .filter(TallerModel.id == id)
        .first()
    )
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    tecnicos = [
        TallerTecnicoResumen(
            id=tecnico.id,
            nombre=tecnico.nombre,
            apellido=tecnico.apellido,
            correo=tecnico.correo,
            telefono=tecnico.telefono,
            esta_activo=tecnico.esta_activo,
            especialidades=[especialidad.nombre for especialidad in tecnico.especialidades],
        )
        for tecnico in taller.usuarios
        if tecnico.rol_id == 3
    ]

    reportes_db = (
        db.query(ReporteModel)
        .options(joinedload(ReporteModel.tecnico))
        .filter(ReporteModel.taller_id == id)
        .order_by(ReporteModel.fecha_creacion.desc(), ReporteModel.id.desc())
        .all()
    )
    reportes = [
        TallerReporteResumen(
            id=reporte.id,
            incidente_id=reporte.incidente_id,
            tipo_reporte=reporte.tipo_reporte,
            motivo=reporte.motivo,
            descripcion=reporte.descripcion,
            estado=reporte.estado,
            fecha_creacion=reporte.fecha_creacion,
            fecha_resolucion=reporte.fecha_resolucion,
            tecnico_id=reporte.tecnico_id,
            tecnico_nombre=reporte.tecnico_nombre,
        )
        for reporte in reportes_db
    ]

    emergencias_db = (
        db.query(IncidenteModel)
        .options(
            joinedload(IncidenteModel.tecnico),
            joinedload(IncidenteModel.usuario),
        )
        .filter(IncidenteModel.taller_id == id)
        .order_by(IncidenteModel.fecha_creacion.desc(), IncidenteModel.id.desc())
        .all()
    )
    emergencias = [
        TallerEmergenciaResumen(
            id=incidente.id,
            estado=incidente.estado,
            prioridad=incidente.prioridad,
            descripcion=incidente.descripcion,
            ubicacion=incidente.ubicacion,
            pago_estado=incidente.pago_estado,
            fecha_creacion=incidente.fecha_creacion,
            tecnico_id=incidente.tecnico_id,
            tecnico_nombre=incidente.tecnico.nombre if incidente.tecnico else None,
            cliente_nombre=incidente.usuario.nombre if incidente.usuario else None,
        )
        for incidente in emergencias_db
    ]

    return TallerDetalleSuperadmin(
        taller=taller,
        estado_habilitacion=bool(taller.estado),
        tecnicos=tecnicos,
        reportes=reportes,
        emergencias=emergencias,
    )


# 4. Leer un taller por su ID (Genérico)
@router.get("/{id}", response_model=Taller)
def leer_taller_por_id(
    id: int,
    db: Session = Depends(deps.get_db)
):
    taller = taller_crud.get(db, id=id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return taller
