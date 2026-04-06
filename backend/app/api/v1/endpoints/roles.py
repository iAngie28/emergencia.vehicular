from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_rol import rol_crud
from app.schemas.rol import Rol, RolCreate, RolUpdate

router = APIRouter()

# 1. Crear un nuevo rol (ej. 'admin', 'taller', 'cliente')
@router.post("/", response_model=Rol)
def crear_rol(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: RolCreate,
    usuario_id: int = 0 # ID del admin que crea el rol para la bitácora
):
    """
    Registra un nuevo nivel de acceso en el sistema.
    """
    rol_existente = rol_crud.obtener_por_nombre(db, nombre=obj_in.nombre)
    if rol_existente:
        raise HTTPException(status_code=400, detail="Este rol ya existe.")
    
    return rol_crud.create(db, obj_in=obj_in, usuario_id=usuario_id)

# 2. Listar todos los roles disponibles
@router.get("/", response_model=List[Rol])
def leer_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna la lista de todos los roles configurados.
    """
    return rol_crud.get_multi(db, skip=skip, limit=limit)

# 3. Eliminar un rol (Cuidado: QA check - no borrar roles en uso)
@router.delete("/{id}", response_model=Rol)
def borrar_rol(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    usuario_id: int
):
    """
    Elimina un rol del sistema y lo registra en la bitácora.
    """
    rol_db = rol_crud.get(db, id=id)
    if not rol_db:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol_crud.remove(db, id=id, usuario_id=usuario_id)