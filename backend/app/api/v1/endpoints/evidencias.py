from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_evidencia import evidencia_crud
from app.schemas.evidencia import Evidencia, EvidenciaCreate, EvidenciaUpdate

router = APIRouter()

# 1. Crear una nueva evidencia (Imagen o Audio)
@router.post("/", response_model=Evidencia)
def crear_evidencia(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: EvidenciaCreate,
    usuario_id: int # ID del usuario que sube el archivo para la bitácora
):
    """
    Registra la URL de una foto o audio asociado a un incidente.
    """
    return evidencia_crud.create(db, obj_in=obj_in, usuario_id=usuario_id)

# 2. Obtener todas las evidencias de un incidente específico (Galería)
@router.get("/incidente/{incidente_id}", response_model=List[Evidencia])
def leer_evidencias_por_incidente(
    incidente_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Retorna la lista de fotos y audios de un incidente. Útil para la galería de la App.
    """
    evidencias = evidencia_crud.obtener_por_incidente(db, incidente_id=incidente_id)
    return evidencias

# 3. Eliminar una evidencia
@router.delete("/{id}", response_model=Evidencia)
def borrar_evidencia(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    usuario_id: int
):
    """
    Elimina un registro de evidencia y lo guarda en la bitácora.
    """
    evidencia = evidencia_crud.get(db, id=id)
    if not evidencia:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")
    return evidencia_crud.remove(db, id=id, usuario_id=usuario_id)