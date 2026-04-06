from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_taller import taller_crud
from app.schemas.taller import Taller, TallerCreate, TallerUpdate

router = APIRouter()

# 1. Registrar un nuevo taller (SaaS onboarding)
@router.post("/", response_model=Taller)
def registrar_taller(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: TallerCreate,
    usuario_id: int = 0 # ID del admin que registra el taller
):
    """
    Registra un taller en la plataforma con sus coordenadas y porcentaje de comisión.
    """
    return taller_crud.create(db, obj_in=obj_in, usuario_id=usuario_id)

# 2. Listar talleres activos (Para el mapa de la App)
@router.get("/activos", response_model=List[Taller])
def leer_talleres_activos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna solo los talleres que están marcados como activos para ser mostrados en el mapa.
    """
    return taller_crud.obtener_activos(db, skip=skip, limit=limit)

# 3. Leer un taller por su ID
@router.get("/{id}", response_model=Taller)
def leer_taller_por_id(
    id: int,
    db: Session = Depends(deps.get_db)
):
    taller = taller_crud.get(db, id=id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return taller

# 4. Actualizar datos (ej. cambiar ubicación o estado)
@router.put("/{id}", response_model=Taller)
def actualizar_taller(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    obj_in: TallerUpdate,
    usuario_id: int
):
    taller_db = taller_crud.get(db, id=id)
    if not taller_db:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return taller_crud.update(db, db_obj=taller_db, obj_in=obj_in, usuario_id=usuario_id)