from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_incidente import incidente_crud
from app.crud.crud_bitacora import bitacora_crud # 👈 Importante para la Regla de Oro
from app.schemas.incidente import Incidente, IncidenteCreate, IncidenteUpdate
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# 1. Reportar incidente (IA) - Mantenemos igual
@router.post("/", response_model=Incidente)
def crear_nuevo_incidente(*, db: Session = Depends(deps.get_db), obj_in: IncidenteCreate):
    return incidente_crud.create(db, obj_in=obj_in, usuario_id=obj_in.usuario_id)

# 2. Pendientes: Solo los que no tienen taller asignado
@router.get("/pendientes", response_model=List[Incidente])
def leer_incidentes_pendientes(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Visualizar auxilios disponibles en Santa Cruz"""
    return incidente_crud.obtener_pendientes(db)

# 3. MI PANEL: Emergencias que YO (como taller) estoy atendiendo
@router.get("/mis-atenciones", response_model=List[Incidente])
def leer_mis_atenciones(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Filtra incidentes por el taller_id del usuario logueado"""
    if not current_user.taller_id:
        raise HTTPException(status_code=400, detail="El usuario no pertenece a un taller")
    
    # Usamos una nueva función que filtra por taller_id
    return incidente_crud.obtener_por_taller(db, taller_id=current_user.taller_id)

# 4. ACEPTAR: El taller toma el incidente
@router.patch("/{id}/aceptar", response_model=Incidente)
def aceptar_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user = Depends(deps.get_current_active_user)
):
    """El taller del token se asigna el incidente automáticamente"""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    if incidente_db.taller_id:
        raise HTTPException(status_code=400, detail="Este incidente ya fue tomado por otro taller")

    # Guardamos estado anterior para bitácora
    anterior = jsonable_encoder(incidente_db)

    # Asignamos el taller del usuario logueado
    actualizado = incidente_crud.asignar_taller(
        db, 
        db_obj=incidente_db, 
        taller_id=current_user.taller_id
    )

    # 📝 BITÁCORA DE AUDITORÍA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="incidente",
        tabla_id=id,
        accion="ACEPTAR_INCIDENTE",
        anterior=anterior,
        nuevo=jsonable_encoder(actualizado)
    )
    
    return actualizado

# 5. FINALIZAR: Cambiar el estado a "atendido"
@router.put("/{id}", response_model=Incidente)
def actualizar_estado_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    obj_in: IncidenteUpdate, # Usamos el schema de actualización
    current_user = Depends(deps.get_current_active_user)
):
    """Actualiza el estado de un incidente (Finalizar servicio)"""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    # QA: Verificar que solo el taller asignado pueda finalizarlo
    if incidente_db.taller_id != current_user.taller_id:
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para finalizar un auxilio que no te pertenece."
        )

    # Guardamos datos para la bitácora
    anterior = jsonable_encoder(incidente_db)

    # Actualizamos usando el CRUD
    actualizado = incidente_crud.update(db, db_obj=incidente_db, obj_in=obj_in)

    # 📝 BITÁCORA DE AUDITORÍA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="incidente",
        tabla_id=id,
        accion="FINALIZAR_AUXILIO",
        anterior=anterior,
        nuevo=jsonable_encoder(actualizado)
    )
    
    return actualizado