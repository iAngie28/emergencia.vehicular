from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate
from decimal import Decimal
from sqlalchemy import func, and_
from typing import Dict, Any


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
    
    def obtener_recaudacion_total(self, db: Session, *, taller_id: int) -> Dict[str, Any]:
        stats = db.query(
            func.sum(self.model.monto).label("total_bruto"),
            func.sum(self.model.comision_plataforma).label("total_comision")
        ).filter(
            self.model.taller_id == taller_id,
            self.model.estado == "completado"
        ).first()

        return {
            "total_recaudado": float(stats.total_bruto or 0),
            "total_comisiones": float(stats.total_comision or 0),
            "neto_taller": float((stats.total_bruto or 0) - (stats.total_comision or 0))
        }
pago_crud = CRUDPago(Pago)