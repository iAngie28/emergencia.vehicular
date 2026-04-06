from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class Bitacora(BaseModel):
    id: int
    usuario_id: Optional[int]
    tabla: str
    accion: str
    valor_anterior: Optional[Any] # Usamos Any porque el JSON puede variar
    valor_nuevo: Optional[Any]
    fecha_hora: datetime

    class Config:
        from_attributes = True # Para que lea de SQLAlchemy