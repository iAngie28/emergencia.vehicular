from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_pago import pago_crud
from app.schemas.pago import Pago, PagoCreate, PagoUpdate

router = APIRouter()

# 1. Registrar un nuevo pago (Calcula la comisión automáticamente en el CRUD)
@router.post("/", response_model=Pago)
def registrar_pago(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: PagoCreate
):
    """
    Registra un pago realizado por un usuario a un taller. 
    El sistema calcula automáticamente el 10% de comisión para la plataforma.
    """
    # Usamos el usuario_id del que paga para la bitácora
    return pago_crud.create(db, obj_in=obj_in)

# 2. Listar todos los pagos de un taller (Para el panel del mecánico)
@router.get("/taller/{taller_id}", response_model=List[Pago])
def leer_pagos_por_taller(
    taller_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Retorna el historial de cobros de un taller específico.
    """
    return pago_crud.obtener_por_taller(db, taller_id=taller_id)

# 3. Actualizar estado del pago (ej. de 'pendiente' a 'completado')
@router.patch("/{id}/estado", response_model=Pago)
def actualizar_estado_pago(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    estado: str,
    usuario_id: int # ID del admin o sistema que valida el pago
):
    """
    Cambia el estado del pago (confirmación de transferencia o QR).
    """
    pago_db = pago_crud.get(db, id=id)
    if not pago_db:
        raise HTTPException(status_code=404, detail="Registro de pago no encontrado")
    
    return pago_crud.update(
        db, 
        db_obj=pago_db, 
        obj_in={"estado": estado}, 
        usuario_id=usuario_id
    )

# 4. Ver todos los pagos (Solo para el Admin del SaaS)
@router.get("/", response_model=List[Pago])
def listar_todos_los_pagos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    return pago_crud.get_multi(db, skip=skip, limit=limit)