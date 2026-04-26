from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.taller_detalle import HorarioTaller
from app.models.usuario import Especialidad
from app.schemas.taller_detalles import (
    HorarioTallerCreate, EspecialidadCreate
) # ❌ Quitamos TallerEspecialidadCreate del import

# CRUD Horarios
class CRUDHorario(CRUDBase[HorarioTaller, HorarioTallerCreate, HorarioTallerCreate]):
    def obtener_por_taller(self, db: Session, *, taller_id: int):
        return db.query(self.model).filter(self.model.taller_id == taller_id).all()

horario_crud = CRUDHorario(HorarioTaller)

# CRUD Especialidades
class CRUDEspecialidad(CRUDBase[Especialidad, EspecialidadCreate, EspecialidadCreate]):
    def obtener_por_nombre(self, db: Session, *, nombre: str):
        return db.query(self.model).filter(self.model.nombre == nombre).first()

especialidad_crud = CRUDEspecialidad(Especialidad)

# ❌ Se eliminó CRUDTallerEspecialidad por completo