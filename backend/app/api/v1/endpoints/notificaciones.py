from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_notificacion import notificacion_crud, token_crud
from app.schemas.notificacion import (
    Notificacion, NotificacionCreate, NotificacionUpdate,
    TokenDispositivo, TokenDispositivoCreate
)

router = APIRouter()

# --- ENDPOINTS DE TOKENS (Dispositivos) ---

@router.post("/tokens", response_model=TokenDispositivo)
def registrar_token_dispositivo(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: TokenDispositivoCreate
):
    """
    Registra el token de Firebase (FCM) del celular del usuario.
    """
    return token_crud.create(db, obj_in=obj_in, usuario_id=obj_in.usuario_id)

# --- ENDPOINTS DE NOTIFICACIONES ---

@router.get("/usuario/{usuario_id}/pendientes", response_model=List[Notificacion])
def leer_notificaciones_no_leidas(
    usuario_id: int,
    db: Session = Depends(deps.get_db)
):
    """
    Lista todas las alertas que el usuario aún no ha visto.
    """
    return notificacion_crud.obtener_no_leidas(db, usuario_id=usuario_id)

@router.patch("/{id}/leer", response_model=Notificacion)
def marcar_como_leida(
    id: int,
    db: Session = Depends(deps.get_db),
    usuario_id: int = 0 # Para la bitácora
):
    """
    Cambia el estado de una notificación a 'leída'.
    """
    notificacion_db = notificacion_crud.get(db, id=id)
    if not notificacion_db:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    return notificacion_crud.update(
        db, 
        db_obj=notificacion_db, 
        obj_in={"leido": True}, 
        usuario_id=usuario_id
    )

@router.post("/", response_model=Notificacion)
def crear_notificacion_manual(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: NotificacionCreate
):
    """
    Permite al sistema enviar una notificación a un usuario (ej. aviso de pago o emergencia).
    """
    return notificacion_crud.create(db, obj_in=obj_in, usuario_id=obj_in.usuario_id)