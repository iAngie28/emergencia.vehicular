from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class IncidenteBase(BaseModel):
    vehiculo_id: int
    usuario_id: int
    taller_id: Optional[int] = None
    latitud: Decimal = Field(..., ge=-90, le=90)
    longitud: Decimal = Field(..., ge=-180, le=180)
    prioridad: str = "media" # 'baja', 'media', 'alta'
    estado: str = "pendiente"

class IncidenteCreate(IncidenteBase):
    # Campos que llena la IA inicialmente
    transcripcion_audio: Optional[str] = None
    clasificacion_ia: Optional[str] = None
    resumen_ia: Optional[str] = None

class IncidenteUpdate(BaseModel):
    taller_id: Optional[int] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None # 'en_proceso', 'atendido', 'cancelado'
    resumen_ia: Optional[str] = None

class Incidente(IncidenteBase):
    id: int
    transcripcion_audio: Optional[str]
    clasificacion_ia: Optional[str]
    resumen_ia: Optional[str]

    class Config:
        from_attributes = True