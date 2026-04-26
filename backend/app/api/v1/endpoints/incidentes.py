from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud.crud_incidente import incidente_crud
from app.crud.crud_bitacora import bitacora_crud # 👈 Importante para la Regla de Oro
from app.schemas.incidente import Incidente, IncidenteCreate, IncidenteUpdate
from fastapi.encoders import jsonable_encoder
from app.models.usuario import Usuario

from app.models.bitacora import Bitacora # 👈 Agrega esta importación

router = APIRouter()

# 1. Reportar incidente (IA) - Mantenemos igual
@router.post("/", response_model=Incidente)
def crear_nuevo_incidente(*, db: Session = Depends(deps.get_db), obj_in: IncidenteCreate):
    return incidente_crud.create(db, obj_in=obj_in, usuario_id=obj_in.usuario_id)

# 2. Pendientes: Solo los que no tienen taller asignado
# Reemplaza tu función leer_incidentes_pendientes por esta:

@router.get("/pendientes", response_model=List[Incidente])
def leer_incidentes_pendientes(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Visualizar auxilios disponibles, filtrando los que este taller ya rechazó."""
    # 1. Traemos todos los incidentes sin taller (taller_id is None)
    incidentes = incidente_crud.obtener_pendientes(db)
    
    if not current_user.taller_id:
        return incidentes

    # 2. Consultamos la Bitácora para ver qué incidentes rechazó este taller
    # Buscamos acciones de 'RECHAZAR_INCIDENTE' o 'RECHAZAR_Y_LIBERAR'
    rechazados_ids = db.query(Bitacora.tabla_id).filter(
        Bitacora.taller_id == current_user.taller_id,
        Bitacora.tabla == "incidente",
        Bitacora.accion.like("RECHAZAR%")
    ).all()
    
    # Convertimos la lista de tuplas en una lista simple de IDs
    lista_negra = [r[0] for r in rechazados_ids]

    # 3. Filtramos: solo devolvemos los que NO están en tu lista negra
    return [i for i in incidentes if i.id not in lista_negra]

# 3. MI PANEL: Emergencias que YO (como taller) estoy atendiendo
@router.get("/mis-atenciones", response_model=List[Incidente])
def leer_mis_atenciones(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Filtra incidentes por el taller_id del usuario logueado"""
    if not current_user.taller_id:
        raise HTTPException(status_code=400, detail="El usuario no pertenece a un taller")
    
    # Usamos una nueva función que filtra por taller_id
    return incidente_crud.obtener_por_taller(db, taller_id=current_user.taller_id)

# 4. ACEPTAR: El taller toma el incidente
@router.patch("/{id}/aceptar", response_model=Incidente)
def aceptar_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user = Depends(deps.get_current_active_user)
):
    """El taller del token se asigna el incidente automáticamente"""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    if incidente_db.taller_id:
        raise HTTPException(status_code=400, detail="Este incidente ya fue tomado por otro taller")

    # Guardamos estado anterior para bitácora
    anterior = jsonable_encoder(incidente_db)

    # Asignamos el taller del usuario logueado
    actualizado = incidente_crud.asignar_taller(
        db, 
        db_obj=incidente_db, 
        taller_id=current_user.taller_id
    )

    # 📝 BITÁCORA DE AUDITORÍA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="incidente",
        tabla_id=id,
        accion="ACEPTAR_INCIDENTE",
        anterior=anterior,
        nuevo=jsonable_encoder(actualizado)
    )
    
    return actualizado
@router.patch("/{id}/asignar-tecnico", response_model=Incidente)
def asignar_tecnico_a_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    tecnico_id: int, # Recibimos el ID del técnico por parámetro
    current_user = Depends(deps.get_current_admin_taller)
):
    """Asigna un técnico del taller a una emergencia ya aceptada."""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db or incidente_db.taller_id != current_user.taller_id:
        raise HTTPException(status_code=403, detail="No puedes asignar técnicos a este incidente.")

    # Opcional: Validar que el técnico pertenezca al mismo taller
    tecnico = db.query(Usuario).filter(Usuario.id == tecnico_id, Usuario.taller_id == current_user.taller_id).first()
    if not tecnico:
        raise HTTPException(status_code=400, detail="El técnico no pertenece a tu taller.")

    anterior = jsonable_encoder(incidente_db)
    actualizado = incidente_crud.asignar_tecnico(db, db_obj=incidente_db, tecnico_id=tecnico_id)

    bitacora_crud.registrar(db, usuario_id=current_user.id, taller_id=current_user.taller_id,
                            tabla="incidente", tabla_id=id, accion="ASIGNAR_TECNICO",
                            anterior=anterior, nuevo=jsonable_encoder(actualizado))
    return actualizado

@router.patch("/{id}/rechazar", response_model=Incidente)
def rechazar_pedido_auxilio(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    motivo: str,
    current_user = Depends(deps.get_current_admin_taller)
):
    """Rechaza el auxilio y lo devuelve a la lista global de pendientes."""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    # Seguridad: Solo el taller que lo tiene o si está libre se puede rechazar
    if incidente_db.taller_id and incidente_db.taller_id != current_user.taller_id:
        raise HTTPException(status_code=403, detail="No puedes rechazar un incidente de otro taller.")

    anterior = jsonable_encoder(incidente_db)

    # 🚩 LA CLAVE DEL ÉXITO: Liberar el incidente
    # Al poner taller y técnico en None y estado en 'pendiente', vuelve a "Disponibles"
    incidente_db.taller_id = None
    incidente_db.tecnico_id = None
    incidente_db.estado = "pendiente"
    incidente_db.motivo_cancelacion = motivo
    
    db.add(incidente_db)
    db.commit()
    db.refresh(incidente_db)

    # 📝 BITÁCORA DE AUDITORÍA (Regla de Oro)
    bitacora_crud.registrar(
        db, 
        usuario_id=current_user.id, 
        taller_id=current_user.taller_id,
        tabla="incidente", 
        tabla_id=id, 
        accion="RECHAZAR_Y_LIBERAR",
        anterior=anterior, 
        nuevo=jsonable_encoder(incidente_db)
    )
    
    return incidente_db

# 5. FINALIZAR: Cambiar el estado a "atendido"
@router.put("/{id}", response_model=Incidente)
def actualizar_estado_incidente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    obj_in: IncidenteUpdate, # Usamos el schema de actualización
    current_user = Depends(deps.get_current_active_user)
):
    """Actualiza el estado de un incidente (Finalizar servicio)"""
    incidente_db = incidente_crud.get(db, id=id)
    if not incidente_db:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    
    # QA: Verificar que solo el taller asignado pueda finalizarlo
    if incidente_db.taller_id != current_user.taller_id:
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para finalizar un auxilio que no te pertenece."
        )

    # Guardamos datos para la bitácora
    anterior = jsonable_encoder(incidente_db)

    # Actualizamos usando el CRUD
    actualizado = incidente_crud.update(db, db_obj=incidente_db, obj_in=obj_in)

    # 📝 BITÁCORA DE AUDITORÍA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="incidente",
        tabla_id=id,
        accion="FINALIZAR_AUXILIO",
        anterior=anterior,
        nuevo=jsonable_encoder(actualizado)
    )
    
    return actualizado