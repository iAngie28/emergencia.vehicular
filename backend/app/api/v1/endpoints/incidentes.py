from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_incidente import incidente_crud
from app.schemas.incidente import Incidente, IncidenteCreate, IncidenteUpdate

router = APIRouter()

# 1. Reportar un nuevo incidente (Aquí entra el JSON de la IA)
@router.post("/", response_model=Incidente)
def crear_nuevo_incidente(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: IncidenteCreate
):
    """
    Registra un incidente con los datos procesados por la IA.
    """
    return incidente_crud.create(db, obj_in=obj_in, usuario_id=obj_in.usuario_id)

# 2. Listar incidentes PENDIENTES (Lo que verán los talleres en su panel)
@router.get("/pendientes", response_model=List[Incidente])
def leer_incidentes_pendientes(
    db: Session = Depends(deps.get_db)
):
    return incidente_crud.obtener_pendientes(db)

# 3. Asignar un taller a un incidente (Cambia estado a 'en_proceso')
@router.patch("/{id}/asignar/{taller_id}", response_model=Incidente)
def asignar_incidente_a_taller(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    taller_id: int,
    usuario_admin_id: int # El ID de quien hace la asignación para la bitácora
):
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    return incidente_crud.asignar_taller(
        db, 
        db_obj=incidente_db, 
        taller_id=taller_id
    )

# 4. Ver historial de un usuario (Cliente)
@router.get("/usuario/{usuario_id}", response_model=List[Incidente])
def leer_historial_usuario(
    usuario_id: int,
    db: Session = Depends(deps.get_db)
):
    return incidente_crud.obtener_por_usuario(db, usuario_id=usuario_id)

# 5. Actualizar estado (ej. de 'en_proceso' a 'atendido')
@router.put("/{id}", response_model=Incidente)
def actualizar_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    obj_in: IncidenteUpdate,
    usuario_id: int
):
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente_crud.update(db, db_obj=incidente_db, obj_in=obj_in, usuario_id=usuario_id)