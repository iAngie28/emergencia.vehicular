from app.crud.base import CRUDBase
from app.models.reporte import Reporte
from app.schemas.reporte import ReporteCreate, ReporteUpdate
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

class CRUDReporte(CRUDBase[Reporte, ReporteCreate, ReporteUpdate]):
    def crear_reporte(self, db: Session, *, obj_in: ReporteCreate, usuario_id: int, taller_id: int) -> Reporte:
        db_obj = Reporte(
            usuario_id=usuario_id,
            incidente_id=obj_in.incidente_id,
            taller_id=taller_id,
            tecnico_id=obj_in.tecnico_id,
            tipo_reporte=obj_in.tipo_reporte,
            motivo=obj_in.motivo,
            descripcion=obj_in.descripcion,
            estado="abierto"
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def obtener_por_incidente(self, db: Session, *, incidente_id: int) -> Optional[Reporte]:
        return db.query(self.model).filter(self.model.incidente_id == incidente_id).first()

    def obtener_por_taller(self, db: Session, *, taller_id: int) -> List[Reporte]:
        return (
            db.query(self.model)
            .filter(self.model.taller_id == taller_id)
            .order_by(self.model.fecha_creacion.desc())
            .all()
        )

    def obtener_todos_taller_reportes(self, db: Session) -> List[Reporte]:
        # El superadmin ve todos los reportes de tipo 'taller'
        return (
            db.query(self.model)
            .filter(self.model.tipo_reporte == "taller")
            .order_by(self.model.fecha_creacion.desc())
            .all()
        )

    def resolver_reporte(self, db: Session, *, db_obj: Reporte, respuesta: str, estado: str = "resuelto") -> Reporte:
        db_obj.respuesta = respuesta
        db_obj.estado = estado
        db_obj.fecha_resolucion = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

reporte_crud = CRUDReporte(Reporte)
