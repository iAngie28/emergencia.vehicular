from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate
from decimal import Decimal

class CRUDPago(CRUDBase[Pago, PagoCreate, PagoUpdate]):
    # Sobreescribimos el create para calcular la comisión automáticamente
    def create(self, db: Session, *, obj_in: PagoCreate) -> Pago:
        obj_data = obj_in.dict()
        
        # Lógica de Negocio: Calcular el 10% de comisión (SaaS mode)
        monto_total = obj_data["monto"]
        obj_data["comision_plataforma"] = monto_total * Decimal("0.10")
        
        db_obj = Pago(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def obtener_por_taller(self, db: Session, *, taller_id: int):
        return db.query(self.model).filter(self.model.taller_id == taller_id).all()

pago_crud = CRUDPago(Pago)