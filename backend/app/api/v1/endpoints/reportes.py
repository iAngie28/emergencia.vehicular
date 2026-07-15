from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app.db.session import get_db
from app.api.deps import get_current_cliente, get_current_active_user
from app.crud.crud_reporte import reporte_crud
from app.crud.crud_incidente import incidente_crud
from app.crud.crud_bitacora import bitacora_crud
from app.schemas.reporte import ReporteCreate, ReporteOut, ReporteUpdate
from app.models.usuario import Usuario
from app.services.notificacion_service import NotificacionService

router = APIRouter()

@router.post("/", response_model=ReporteOut, status_code=status.HTTP_201_CREATED)
def crear_reporte(
    reporte_in: ReporteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_cliente)
) -> Any:
    # 1. Validar que el incidente existe y pertenece al cliente
    incidente = incidente_crud.get(db, id=reporte_in.incidente_id)
    if not incidente:
        raise HTTPException(status_code=404, detail="El incidente no existe.")
    
    if incidente.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para reportar este incidente."
        )

    # 2. Validar tipo de reporte
    if reporte_in.tipo_reporte not in ("taller", "tecnico"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de reporte debe ser 'taller' o 'tecnico'."
        )

    # 3. Validar que el incidente tenga taller asignado
    if not incidente.taller_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede reportar un incidente que no tiene un taller asignado."
        )

    # 4. Validar técnico si el tipo de reporte es técnico
    if reporte_in.tipo_reporte == "tecnico":
        if not reporte_in.tecnico_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se debe especificar el ID del técnico a reportar."
            )
        if incidente.tecnico_id != reporte_in.tecnico_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El técnico especificado no participó en este incidente."
            )

    # 5. Validar que no exista ya un reporte del mismo tipo para el incidente
    reporte_existente = reporte_crud.obtener_por_incidente_y_tipo(
        db,
        incidente_id=reporte_in.incidente_id,
        tipo_reporte=reporte_in.tipo_reporte,
    )
    if reporte_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un reporte de {reporte_in.tipo_reporte} registrado para este incidente."
        )

    # 6. Crear el reporte
    reporte = reporte_crud.crear_reporte(
        db,
        obj_in=reporte_in,
        usuario_id=current_user.id,
        taller_id=incidente.taller_id
    )

    # 7. Registrar en bitácora
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=incidente.taller_id,
        tabla="reporte",
        tabla_id=reporte.id,
        accion="CREATE_REPORTE",
        nuevo={
            "tipo_reporte": reporte.tipo_reporte,
            "motivo": reporte.motivo
        }
    )

    # 8. Notificar a los responsables correctos.
    # Reporte de técnico: admins del taller. Reporte de taller: superadmins.
    if reporte.tipo_reporte == "tecnico":
        destinatarios = db.query(Usuario).filter(
            Usuario.taller_id == reporte.taller_id,
            Usuario.rol_id == 1
        ).all()
    else:
        destinatarios = db.query(Usuario).filter(Usuario.rol_id == 4).all()

    for destinatario in destinatarios:
        NotificacionService.crear_notificacion(
            db,
            usuario_id=destinatario.id,
            titulo=f"Nuevo Reporte de {reporte.tipo_reporte.capitalize()}",
            mensaje=f"Se ha registrado un reporte contra el {reporte.tipo_reporte} por el motivo: {reporte.motivo}.",
            tipo="reporte_registrado",
            incidente_id=incidente.id,
            extra_data={
                "tipo_reporte": reporte.tipo_reporte,
                "reporte_id": reporte.id,
                "taller_id": reporte.taller_id,
                "tecnico_id": reporte.tecnico_id,
            }
        )

    return reporte


@router.get("/", response_model=List[ReporteOut])
def listar_reportes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    # Si el usuario tiene taller_id activo (Admin de Taller real o Superadmin Impersonando Taller)
    if current_user.taller_id and current_user.rol_id == 1:
        return reporte_crud.obtener_tecnicos_por_taller(db, taller_id=current_user.taller_id)

    # Si es Super Administrador actuando globalmente sin impersonar a un taller específico
    original_rol_id = getattr(current_user, "original_rol_id", current_user.rol_id)
    if original_rol_id == 4 and current_user.rol_id == 4:
        return reporte_crud.obtener_todos_taller_reportes(db)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para ver el listado de reportes."
    )


@router.get("/incidente/{incidente_id}/mi-reporte", response_model=ReporteOut)
def obtener_mi_reporte_por_incidente(
    incidente_id: int,
    tipo_reporte: Optional[str] = Query(None, description="Filtra por 'taller' o 'tecnico'"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_cliente)
) -> Any:
    if tipo_reporte is not None and tipo_reporte not in ("taller", "tecnico"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El tipo de reporte debe ser 'taller' o 'tecnico'."
        )

    reporte = reporte_crud.obtener_ultimo_por_incidente(
        db,
        incidente_id=incidente_id,
        usuario_id=current_user.id,
        tipo_reporte=tipo_reporte,
        priorizar_respondidos=True,
    )

    if not reporte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un reporte tuyo para este incidente."
        )

    return reporte


@router.patch("/{id}/responder", response_model=ReporteOut)
def responder_reporte(
    id: int,
    reporte_update: ReporteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
) -> Any:
    reporte = reporte_crud.get(db, id=id)
    if not reporte:
        raise HTTPException(status_code=404, detail="El reporte no existe.")

    original_rol_id = getattr(current_user, "original_rol_id", current_user.rol_id)
    es_superadmin_global = original_rol_id == 4 and current_user.rol_id == 4

    # Validar permisos
    if es_superadmin_global:
        # Superadministrador puede responder a reportes de tipo 'taller'
        if reporte.tipo_reporte != "taller":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Los Superadministradores solo pueden responder reportes de talleres."
            )
    elif current_user.rol_id == 1:
        # Administrador del taller puede responder a reportes de tipo 'tecnico' de su propio taller
        if reporte.tipo_reporte != "tecnico" or reporte.taller_id != current_user.taller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para responder a este reporte."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes."
        )

    # Actualizar reporte
    reporte_actualizado = reporte_crud.resolver_reporte(
        db,
        db_obj=reporte,
        respuesta=reporte_update.respuesta,
        estado=reporte_update.estado
    )

    # Registrar en bitácora
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=reporte.taller_id if current_user.rol_id == 1 else None,
        tabla="reporte",
        tabla_id=reporte.id,
        accion="RESOLVE_REPORTE",
        nuevo={
            "respuesta": reporte_update.respuesta,
            "estado": reporte_update.estado
        }
    )

    # Notificar al cliente creador del reporte
    NotificacionService.crear_notificacion(
        db,
        usuario_id=reporte.usuario_id,
        titulo="Respuesta a tu reporte",
        mensaje=f"Tu reporte sobre el incidente #{reporte.incidente_id} ha sido respondido.",
        tipo="reporte_respondido",
        incidente_id=reporte.incidente_id
    )

    return reporte_actualizado
