from sqlalchemy.orm import Session
from app.models.bitacora import Bitacora
from datetime import datetime
from typing import Optional, Any, Dict

class CRUDBitacora:
    def registrar(self, db: Session, *, usuario_id: Optional[int] = None, taller_id: Optional[int] = None, tabla: str, accion: str, anterior: dict = None, nuevo: dict = None, tabla_id: int = None):
        db_usuario_id = usuario_id if usuario_id and usuario_id > 0 else None
        db_obj = Bitacora(
            usuario_id=db_usuario_id,
            taller_id=taller_id,
            tabla=tabla,
            tabla_id=tabla_id,
            accion=accion,
            valor_anterior=anterior,
            valor_nuevo=nuevo,
            fecha_hora=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        return db_obj

bitacora_crud = CRUDBitacora()