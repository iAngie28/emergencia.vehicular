from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from app.models.bitacora import Bitacora
from app.models.usuario import Usuario # 🚩 Importamos el modelo de Usuario
from app.schemas.bitacora import Bitacora as BitacoraSchema

router = APIRouter()

# 🚩 Quitamos el response_model estricto para que deje pasar el "usuario_nombre"
@router.get("/")
def leer_historial_auditoria(
    db: Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100,
    current_user = Depends(deps.get_current_admin_taller) # 👈 CANDADO APLICADO: Solo Admin Web
):
    """
    Retorna la lista de movimientos registrados SOLO para el taller del usuario actual,
    incluyendo el nombre del responsable.
    """
    if not current_user.taller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene un taller asignado para ver auditoría."
        )

    # 1. Hacemos un JOIN con Usuario para traer el nombre de una vez (optimizado)
    resultados = (
        db.query(Bitacora, Usuario.nombre)
        .outerjoin(Usuario, Bitacora.usuario_id == Usuario.id)
        .filter(Bitacora.taller_id == current_user.taller_id)
        .order_by(Bitacora.fecha_hora.desc())
        .offset(skip).limit(limit).all()
    )

    # 2. Armamos la lista de diccionarios inyectando el nombre
    logs_formateados = []
    for bitacora, nombre_usuario in resultados:
        # Convertimos el registro de SQLAlchemy a un diccionario normal
        log_dict = {c.name: getattr(bitacora, c.name) for c in bitacora.__table__.columns}
        
        # Agregamos nuestro nuevo campo
        log_dict["usuario_nombre"] = nombre_usuario if nombre_usuario else "Sistema"
        
        logs_formateados.append(log_dict)

    return logs_formateados