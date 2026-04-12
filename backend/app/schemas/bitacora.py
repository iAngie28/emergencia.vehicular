from pydantic import BaseModel  # <--- ESTO ES LO QUE FALTA
from datetime import datetime
from typing import Optional

class BitacoraBase(BaseModel):
    tabla: str
    tabla_id: int
    accion: str
    valor_anterior: Optional[dict] = None
    valor_nuevo: Optional[dict] = None
    taller_id: int  # <-- ¡No te olvides de este!

class Bitacora(BitacoraBase):
    id: int
    fecha_hora: datetime
    usuario_id: Optional[int]

    class Config:
        from_attributes = True