from sqlalchemy.orm import Session
from app.models.bitacora import Bitacora
from datetime import datetime
from typing import Optional
from fastapi.encoders import jsonable_encoder # 👈 Importante para convertir Decimals

class CRUDBitacora:
    def registrar(self, db: Session, *, 
                  usuario_id: Optional[int] = None, 
                  taller_id: Optional[int] = None, 
                  tabla: str, 
                  accion: str, 
                  anterior: dict = None, 
                  nuevo: dict = None, 
                  tabla_id: int = None):
        
        db_usuario_id = usuario_id if usuario_id and usuario_id > 0 else None
        
        # 🧹 Sanitize: Convertimos Decimals (lat/lng) a floats para que sean JSON serializables
        val_anterior = jsonable_encoder(anterior) if anterior else None
        val_nuevo = jsonable_encoder(nuevo) if nuevo else None

        db_obj = Bitacora(
            usuario_id=db_usuario_id,
            taller_id=taller_id,
            tabla=tabla,
            tabla_id=tabla_id,
            accion=accion,
            valor_anterior=val_anterior, # 👈 Usamos la versión limpia
            valor_nuevo=val_nuevo,       # 👈 Usamos la versión limpia
            fecha_hora=datetime.now()
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

bitacora_crud = CRUDBitacora()