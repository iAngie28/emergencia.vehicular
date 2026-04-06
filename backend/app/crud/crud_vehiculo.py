from app.crud.base import CRUDBase
from app.models.vehiculo import Vehiculo
from app.schemas.vehiculo import VehiculoCreate, VehiculoUpdate
from sqlalchemy.orm import Session

class CRUDVehiculo(CRUDBase[Vehiculo, VehiculoCreate, VehiculoUpdate]):
    # Aquí puedes agregar funciones específicas que NO sean genéricas
    def obtener_por_placa(self, db: Session, *, placa: str):
        return db.query(self.model).filter(self.model.placa == placa).first()

vehiculo_crud = CRUDVehiculo(Vehiculo)