from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_vehiculo import vehiculo_crud # Asegúrate de que el nombre coincida
from app.schemas.vehiculo import Vehiculo, VehiculoCreate, VehiculoUpdate

router = APIRouter()

# 1. Registrar un vehículo (El cliente asocia su auto a su cuenta)
@router.post("/", response_model=Vehiculo)
def registrar_vehiculo(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: VehiculoCreate,
    usuario_id: int # El ID del dueño para la bitácora
):
    # QA Check: La placa es única
    db_vehiculo = vehiculo_crud.obtener_por_placa(db, placa=obj_in.placa)
    if db_vehiculo:
        raise HTTPException(status_code=400, detail="Ya existe un vehículo registrado con esta placa.")
    
    return vehiculo_crud.create(db, obj_in=obj_in, usuario_id=usuario_id)

# 2. Leer un vehículo por su ID
@router.get("/{id}", response_model=Vehiculo)
def leer_vehiculo(id: int, db: Session = Depends(deps.get_db)):
    db_vehiculo = vehiculo_crud.get(db, id=id)
    if not db_vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

# 3. Listar vehículos de un usuario específico
@router.get("/usuario/{propietario_id}", response_model=List[Vehiculo])
def listar_mis_vehiculos(propietario_id: int, db: Session = Depends(deps.get_db)):
    return db.query(vehiculo_crud.model).filter(vehiculo_crud.model.usuario_id == propietario_id).all()

# 4. Actualizar datos (ej. cambiar color o seguro)
@router.put("/{id}", response_model=Vehiculo)
def actualizar_vehiculo(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    obj_in: VehiculoUpdate,
    usuario_id: int
):
    db_vehiculo = vehiculo_crud.get(db, id=id)
    if not db_vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo_crud.update(db, db_obj=db_vehiculo, obj_in=obj_in, usuario_id=usuario_id)