from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.taller import Taller
from app.schemas.taller import TallerCreate, TallerUpdate

class CRUDTaller(CRUDBase[Taller, TallerCreate, TallerUpdate]):
    
    # Función específica para buscar talleres activos (Para el mapa)
    def obtener_activos(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(self.model.estado == True).offset(skip).limit(limit).all()

    # Podrías agregar aquí una función de búsqueda por cercanía (Haversine) más adelante
    def buscar_cercanos(self, db: Session, lat: float, lon: float, radio_km: float = 10):
        # Esta lógica se puede implementar con una query de SQL nativo o GeoAlchemy
        pass

taller_crud = CRUDTaller(Taller)