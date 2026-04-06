from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.crud_usuario import usuario_crud
from app.schemas.usuario import Usuario, UsuarioCreate
from app.api import deps # Aquí debes tener tu función get_db

router = APIRouter()

@router.post("/", response_model=Usuario)
def registrar_usuario(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: UsuarioCreate
):
    # QA Check: ¿Ya existe el correo?
    usuario_existente = usuario_crud.obtener_por_correo(db, correo=obj_in.correo)
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Este correo ya está registrado en el sistema."
        )
    
    # Si todo está bien, creamos
    return usuario_crud.create(db, obj_in=obj_in)

@router.get("/", response_model=List[Usuario])
def listar_usuarios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    return usuario_crud.get_multi(db, skip=skip, limit=limit)