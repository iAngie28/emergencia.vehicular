from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- SCHEMAS PARA TOKEN DISPOSITIVO ---
class TokenDispositivoBase(BaseModel):
    usuario_id: int
    token_fcm: str
    plataforma: str # 'android', 'ios', 'web'

class TokenDispositivoCreate(TokenDispositivoBase):
    pass

class TokenDispositivo(TokenDispositivoBase):
    id: int
    ultima_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True

# --- SCHEMAS PARA NOTIFICACIÓN ---
class NotificacionBase(BaseModel):
    usuario_id: int
    incidente_id: Optional[int] = None
    titulo: str
    mensaje: str
    tipo: str # 'emergencia', 'pago', 'sistema'

class NotificacionCreate(NotificacionBase):
    pass

class NotificacionUpdate(BaseModel):
    leido: bool = True

class Notificacion(NotificacionBase):
    id: int
    leido: bool
    fecha_envio: datetime

    class Config:
        from_attributes = True