from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.incidente import Incidente
from app.schemas.incidente import IncidenteCreate, IncidenteUpdate
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import func, and_
from app.models.usuario import Usuario
from app.models.pago import Pago

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
    
    def obtener_por_taller(self, db: Session, *, taller_id: int):
        return db.query(self.model).filter(self.model.taller_id == taller_id).all()


    # Función para filtrar por el cliente (Para que el usuario vea su historial)
    def obtener_por_usuario(self, db: Session, *, usuario_id: int):
        return db.query(self.model).filter(self.model.usuario_id == usuario_id).all()
    
    def asignar_tecnico(self, db: Session, *, db_obj: Incidente, tecnico_id: int) -> Incidente:
        """Asigna un técnico específico del taller al incidente."""
        return self.update(db, db_obj=db_obj, obj_in={"tecnico_id": tecnico_id})

    def rechazar_incidente(self, db: Session, *, db_obj: Incidente, motivo: str) -> Incidente:
        """Marca el incidente como rechazado por el taller."""
        update_data = {
            "estado": "rechazado",
            "motivo_cancelacion": motivo,
            "taller_id": None # Lo liberamos para que otros talleres NO lo vean o se sepa que fue devuelto
        }
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def obtener_historial_taller(
        self, 
        db: Session, 
        *, 
        taller_id: int, 
        fecha_inicio: Optional[datetime] = None, 
        fecha_fin: Optional[datetime] = None,
        estados: Optional[List[str]] = None, # 👈 Lista de estados
        tecnico_id: Optional[int] = None      # 👈 ID de técnico
    ) -> List[Incidente]:
        query = db.query(self.model).filter(self.model.taller_id == taller_id)
        
        # Cargar las relaciones de técnico y pagos
        query = query.options(joinedload(self.model.tecnico), joinedload(self.model.pagos))
        
        # Filtrado por múltiples estados
        if estados and len(estados) > 0:
            query = query.filter(self.model.estado.in_(estados))
        else:
            # Comportamiento por defecto si no hay nada seleccionado
            query = query.filter(self.model.estado.in_(["atendido", "cancelado"]))

        # Filtrado por técnico
        if tecnico_id:
            query = query.filter(self.model.tecnico_id == tecnico_id)

        if fecha_inicio:
            query = query.filter(self.model.fecha_creacion >= fecha_inicio)
        if fecha_fin:
            query = query.filter(self.model.fecha_creacion <= fecha_fin)
            
        return query.order_by(self.model.fecha_creacion.desc()).all()
    

    def obtener_metricas_taller(self, db: Session, *, taller_id: int, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None, estados: Optional[List[str]] = None, tecnico_id: Optional[int] = None) -> Dict[str, Any]:
        """Calcula los KPIs para la pestaña de historial, respetando filtros aplicados."""
        
        # 1. Atenciones por Técnico
        query_tecnico = db.query(
            Usuario.nombre, func.count(self.model.id).label("total")
        ).join(Usuario, self.model.tecnico_id == Usuario.id)\
         .filter(self.model.taller_id == taller_id, self.model.estado == "atendido")
        
        # Aplicar filtros a atenciones por técnico
        if tecnico_id:
            query_tecnico = query_tecnico.filter(self.model.tecnico_id == tecnico_id)
        if fecha_inicio:
            query_tecnico = query_tecnico.filter(self.model.fecha_creacion >= fecha_inicio)
        if fecha_fin:
            query_tecnico = query_tecnico.filter(self.model.fecha_creacion <= fecha_fin)
        
        por_tecnico = query_tecnico.group_by(Usuario.nombre).all()

        # 2. Recaudación Total del Taller (Restando el 10% de la plataforma)
        # Filtramos pagos que correspondan a incidentes del taller y aplicamos filtros
        query_pago = db.query(Pago).filter(
            Pago.taller_id == taller_id, 
            Pago.estado == "completado"
        )
        
        # Aplicar filtros de incidentes a pagos
        if estados or fecha_inicio or fecha_fin or tecnico_id:
            query_pago = query_pago.join(
                Incidente, Pago.incidente_id == Incidente.id
            )
            
            if estados:
                query_pago = query_pago.filter(Incidente.estado.in_(estados))
            if tecnico_id:
                query_pago = query_pago.filter(Incidente.tecnico_id == tecnico_id)
            if fecha_inicio:
                query_pago = query_pago.filter(Incidente.fecha_creacion >= fecha_inicio)
            if fecha_fin:
                query_pago = query_pago.filter(Incidente.fecha_creacion <= fecha_fin)
        
        pagos = query_pago.all()
        
        total_bruto = sum(p.monto for p in pagos) if pagos else 0
        total_comision = sum(p.comision_plataforma for p in pagos) if pagos else 0

        return {
            "atenciones_por_tecnico": [{"tecnico": t[0], "cantidad": t[1]} for t in por_tecnico],
            "finanzas": {
                "recaudado_neto": float(total_bruto - total_comision),
                "recaudado_bruto": float(total_bruto)
            }
        }
    
incidente_crud = CRUDIncidente(Incidente)