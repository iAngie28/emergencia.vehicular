from app.crud.base import CRUDBase
from app.models.evidencia import Evidencia
from app.schemas.evidencia import EvidenciaCreate, EvidenciaUpdate
from sqlalchemy.orm import Session
from typing import List

class CRUDEvidencia(CRUDBase[Evidencia, EvidenciaCreate, EvidenciaUpdate]):
    # Función específica: Útil para mostrar la galería del incidente en la App
    def obtener_por_incidente(self, db: Session, *, incidente_id: int) -> List[Evidencia]:
        return db.query(self.model).filter(self.model.incidente_id == incidente_id).all()

evidencia_crud = CRUDEvidencia(Evidencia)