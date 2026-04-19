from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.usuario import UsuarioUpdate

from app.api import deps
from app.crud.crud_usuario import usuario_crud
from app.crud.crud_bitacora import bitacora_crud # 🚩 Tu CRUD
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.usuario import Usuario as UsuarioSchema, UsuarioCreate

router = APIRouter()

@router.get("/me", response_model=UsuarioSchema)
def leer_usuario_actual(current_user = Depends(deps.get_current_user)):
    return current_user

@router.get("/mis-administradores", response_model=List[UsuarioSchema])
def listar_admins_de_mi_taller(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_taller)
):
    return db.query(UsuarioModel).filter(
        UsuarioModel.taller_id == current_user.taller_id,
        UsuarioModel.rol_id == 1
    ).all()
@router.post("/nuevo-colega", response_model=UsuarioSchema)
def crear_administrador_adicional(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UsuarioCreate,
    current_user = Depends(deps.get_current_admin_taller)
):
    if usuario_crud.get_by_email(db, email=user_in.correo):
        raise HTTPException(status_code=400, detail="El correo ya existe.")
    
    user_in.rol_id = 1
    user_in.taller_id = current_user.taller_id
    nuevo_usuario = usuario_crud.create(db, obj_in=user_in)

    # 🚩 BITÁCORA (Actualizada con teléfono)
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="usuario",
        tabla_id=nuevo_usuario.id,
        accion="Crear_USUARIO",
        nuevo={
            "nombre": nuevo_usuario.nombre, 
            "correo": nuevo_usuario.correo,
            "telefono": nuevo_usuario.telefono # 🚩 Ahora lo guardamos
        }
    )
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioSchema)
def actualizar_administrador(
    usuario_id: int,
    *,
    db: Session = Depends(deps.get_db),
    user_in: UsuarioUpdate,
    current_user = Depends(deps.get_current_admin_taller)
):
    # QA: Solo puedes editar admins de TU taller
    usuario_db = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id,
        UsuarioModel.taller_id == current_user.taller_id
    ).first()

    if not usuario_db:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")

    anterior_datos = {
        "nombre": usuario_db.nombre, 
        "correo": usuario_db.correo, 
        "telefono": usuario_db.telefono
    }

    usuario_actualizado = usuario_crud.update(db, db_obj=usuario_db, obj_in=user_in)

    # 🚩 BITÁCORA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="usuario",
        tabla_id=usuario_id,
        accion="ACTUALIZAR_USUARIO",
        anterior=anterior_datos,
        nuevo=user_in.dict(exclude_unset=True)
    )
    return usuario_actualizado

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_administrador(
    usuario_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_taller)
):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id, 
        UsuarioModel.taller_id == current_user.taller_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="No encontrado.")
    if usuario.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo.")

    # Guardamos datos para la bitácora antes de borrar
    datos_borrado = {"nombre": usuario.nombre, "correo": usuario.correo}
    id_borrado = usuario.id

    db.delete(usuario)
    db.commit()

    # 🚩 BITÁCORA
    bitacora_crud.registrar(
        db,
        usuario_id=current_user.id,
        taller_id=current_user.taller_id,
        tabla="usuario",
        tabla_id=id_borrado,
        accion="ELIMINAR_USUARIO",
        anterior=datos_borrado
    )
    
    return None