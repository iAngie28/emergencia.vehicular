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
    current_user = Depends(deps.get_current_active_user)
):
    """
    Retorna la lista de movimientos registrados.
    - Admin de taller: solo ve los registros de su taller.
    - Superadmin sin impersonar: ve la bitácora global.
    """
    original_rol_id = getattr(current_user, "original_rol_id", current_user.rol_id)
    es_superadmin_global = original_rol_id == 4 and current_user.rol_id == 4
    es_admin_taller = current_user.rol_id == 1

    if not es_superadmin_global and not es_admin_taller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requieren permisos de Administrador o Super Administrador.",
        )

    if es_admin_taller and not current_user.taller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene un taller asignado para ver auditoría."
        )

    # 1. Hacemos un JOIN con Usuario para traer el nombre de una vez (optimizado)
    query = (
        db.query(Bitacora, Usuario.nombre)
        .outerjoin(Usuario, Bitacora.usuario_id == Usuario.id)
        .order_by(Bitacora.fecha_hora.desc())
    )

    if es_admin_taller:
        query = query.filter(Bitacora.taller_id == current_user.taller_id)

    resultados = query.offset(skip).limit(limit).all()

    # 2. Armamos la lista de diccionarios inyectando el nombre
    logs_formateados = []
    for bitacora, nombre_usuario in resultados:
        # Convertimos el registro de SQLAlchemy a un diccionario normal
        log_dict = {c.name: getattr(bitacora, c.name) for c in bitacora.__table__.columns}
        
        # Agregamos nuestro nuevo campo
        log_dict["usuario_nombre"] = nombre_usuario if nombre_usuario else "Sistema"
        
        logs_formateados.append(log_dict)

    return logs_formateados
