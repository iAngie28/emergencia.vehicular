from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.bitacora import Bitacora
from app.schemas.bitacora import Bitacora as BitacoraSchema

router = APIRouter()

@router.get("/", response_model=List[BitacoraSchema])
def leer_historial_auditoria(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100,
    current_user = Depends(deps.get_current_user) # <--- Ahora esto ya no dará error
):
    """
    Retorna la lista de movimientos registrados SOLO para el taller del usuario actual.
    """
    
    # 2. VALIDACIÓN DE TENANT:
    # Verificamos que el usuario pertenezca a un taller (evita leaks de datos)
    if not current_user.taller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene un taller asignado para ver auditoría."
        )

    # 3. AISLAMIENTO DE DATOS:
    # Filtramos la consulta por taller_id para que el Admin A no vea al Admin B
    query = db.query(Bitacora).filter(Bitacora.taller_id == current_user.taller_id)
    
    # 4. EJECUCIÓN:
    return query.order_by(Bitacora.fecha_hora.desc()).offset(skip).limit(limit).all()