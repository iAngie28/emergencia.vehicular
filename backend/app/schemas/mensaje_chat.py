from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MensajeChatBase(BaseModel):
    incidente_id: int
    remitente_id: int
    contenido: str
    tipo: str = "texto"


class MensajeChatCreate(MensajeChatBase):
    pass


class MensajeChatOut(MensajeChatBase):
    id: int
    fecha_envio: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
