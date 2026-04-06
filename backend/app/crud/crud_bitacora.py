from sqlalchemy.orm import Session
from app.models.bitacora import Bitacora
from datetime import datetime

class CRUDBitacora:
    def registrar(self, db: Session, *, usuario_id: int, tabla: str, accion: str, anterior: dict = None, nuevo: dict = None):
        if usuario_id == 0 or usuario_id is None:
            final_user_id = None
        else:
            final_user_id = usuario_id
        
        db_obj = Bitacora(
            usuario_id=final_user_id,
            tabla=tabla,
            accion=accion,
            valor_anterior=anterior,
            valor_nuevo=nuevo,
            fecha_hora=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        return db_obj

bitacora_crud = CRUDBitacora()