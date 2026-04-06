from app.crud.base import CRUDBase
from app.models.rol import Rol
from app.schemas.rol import RolCreate, RolUpdate
from sqlalchemy.orm import Session

class CRUDRol(CRUDBase[Rol, RolCreate, RolUpdate]):
    # Función extra para buscar por nombre (útil para inicializar la DB)
    def obtener_por_nombre(self, db: Session, *, nombre: str) -> Rol:
        return db.query(self.model).filter(self.model.nombre == nombre).first()

rol_crud = CRUDRol(Rol)