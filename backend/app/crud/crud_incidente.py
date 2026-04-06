from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.incidente import Incidente
from app.schemas.incidente import IncidenteCreate, IncidenteUpdate

class CRUDIncidente(CRUDBase[Incidente, IncidenteCreate, IncidenteUpdate]):
    
    # Función para que un taller "tome" el incidente
    def asignar_taller(self, db: Session, *, db_obj: Incidente, taller_id: int) -> Incidente:
        update_data = {
            "taller_id": taller_id,
            "estado": "en_proceso"
        }
        return self.update(db, db_obj=db_obj, obj_in=update_data)

    # Función para obtener incidentes pendientes (Para que los talleres los vean)
    def obtener_pendientes(self, db: Session):
        return db.query(self.model).filter(self.model.estado == "pendiente").all()

    # Función para filtrar por el cliente (Para que el usuario vea su historial)
    def obtener_por_usuario(self, db: Session, *, usuario_id: int):
        return db.query(self.model).filter(self.model.usuario_id == usuario_id).all()

incidente_crud = CRUDIncidente(Incidente)