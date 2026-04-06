from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_bitacora import bitacora_crud
from app.schemas.bitacora import Bitacora as BitacoraSchema

router = APIRouter()

@router.get("/", response_model=List[BitacoraSchema])
def leer_historial_auditoria(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100
):
    """
    Retorna la lista de todos los movimientos registrados en el sistema.
    """
    # Usamos una consulta simple para traer los datos
    from app.models.bitacora import Bitacora
    return db.query(Bitacora).order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()