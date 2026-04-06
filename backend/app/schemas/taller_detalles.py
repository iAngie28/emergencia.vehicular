from pydantic import BaseModel
from typing import Optional, List
from datetime import time

# --- HORARIOS ---
class HorarioTallerBase(BaseModel):
    taller_id: int
    dia: str # 'lunes', 'martes'...
    hora_apertura: time
    hora_cierre: time

class HorarioTallerCreate(HorarioTallerBase):
    pass

class HorarioTaller(HorarioTallerBase):
    id: int
    class Config:
        from_attributes = True

# --- ESPECIALIDADES ---
class EspecialidadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EspecialidadCreate(EspecialidadBase):
    pass

class Especialidad(EspecialidadBase):
    id: int
    class Config:
        from_attributes = True

# --- RELACIÓN TALLER-ESPECIALIDAD (Tabla Intermedia) ---
class TallerEspecialidadBase(BaseModel):
    taller_id: int
    especialidad_id: int
    nivel_experiencia: str # 'basico', 'experto'

class TallerEspecialidadCreate(TallerEspecialidadBase):
    pass