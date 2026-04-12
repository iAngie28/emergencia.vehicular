from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.crud.crud_taller_detalles import horario_crud, especialidad_crud, taller_especialidad_crud
from app.schemas.taller_detalles import (
    HorarioTaller, HorarioTallerCreate,
    Especialidad, EspecialidadCreate,
    TallerEspecialidadBase, TallerEspecialidadCreate
)

router = APIRouter()

# --- HORARIOS ---
@router.post("/horarios", response_model=HorarioTaller)
def agregar_horario(
    obj_in: HorarioTallerCreate, 
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_taller) # 👈 CANDADO APLICADO
):
    """Define la hora de apertura y cierre para un día específico."""
    return horario_crud.create(
        db, 
        obj_in=obj_in,
        usuario_id=current_user.id,        
        taller_id=current_user.taller_id   
    )

@router.get("/taller/{taller_id}/horarios", response_model=List[HorarioTaller])
def leer_horarios_taller(taller_id: int, db: Session = Depends(deps.get_db)):
    return horario_crud.obtener_por_taller(db, taller_id=taller_id)

# --- ESPECIALIDADES (Catálogo General) ---
@router.post("/especialidades", response_model=Especialidad)
def crear_especialidad(
    obj_in: EspecialidadCreate, 
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_taller) # 👈 CANDADO APLICADO
):
    """Crea una especialidad en el catálogo (ej: Frenos, Motor, Pintura)."""
    existente = especialidad_crud.obtener_por_nombre(db, nombre=obj_in.nombre)
    if existente:
        raise HTTPException(status_code=400, detail="Especialidad ya existe")
    
    return especialidad_crud.create(
        db, 
        obj_in=obj_in,
        usuario_id=current_user.id,        
        taller_id=current_user.taller_id   
    )

@router.get("/especialidades", response_model=List[Especialidad])
def listar_especialidades(db: Session = Depends(deps.get_db)):
    return especialidad_crud.get_multi(db)

# --- TALLER <-> ESPECIALIDAD (Vinculación) ---
@router.post("/vincular-especialidad", response_model=TallerEspecialidadBase)
def vincular_taller_con_especialidad(
    obj_in: TallerEspecialidadCreate, 
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_admin_taller) # 👈 CANDADO APLICADO
):
    """Asigna una especialidad a un taller con su nivel de experiencia."""
    return taller_especialidad_crud.create(
        db, 
        obj_in=obj_in,
        usuario_id=current_user.id,        
        taller_id=current_user.taller_id   
    )

@router.get("/taller/{taller_id}/especialidades", response_model=List[TallerEspecialidadBase])
def leer_especialidades_taller(taller_id: int, db: Session = Depends(deps.get_db)):
    return taller_especialidad_crud.obtener_especialidades_de_taller(db, taller_id=taller_id)