from pydantic import BaseModel, Field, root_validator
from typing import Optional, Dict, Any
from decimal import Decimal

# Esquema para mostrar info básica del técnico
class TecnicoInfo(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

class IncidenteBase(BaseModel):
    vehiculo_id: int
    usuario_id: int
    taller_id: Optional[int] = None
    tecnico_id: Optional[int] = None
    latitud: Decimal = Field(..., ge=-90, le=90)
    longitud: Decimal = Field(..., ge=-180, le=180)
    prioridad: str = "media" 
    estado: str = "pendiente"
    pago_estado: str = "pendiente"
    telefono_cliente: str = "No disponible"
    motivo_cancelacion: Optional[str] = None

    class Config:
        from_attributes = True

class IncidenteCreate(IncidenteBase):
    transcripcion_audio: Optional[str] = None
    clasificacion_ia: Optional[str] = None
    resumen_ia: Optional[str] = None

class IncidenteUpdate(BaseModel):
    taller_id: Optional[int] = None
    tecnico_id: Optional[int] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None 
    pago_estado: Optional[str] = None
    motivo_cancelacion: Optional[str] = None
    resumen_ia: Optional[str] = None

class Incidente(IncidenteBase):
    id: int
    transcripcion_audio: Optional[str] = None
    clasificacion_ia: Optional[str] = None
    resumen_ia: Optional[str] = None
    
    # 🚩 Pydantic se encargará de mapear la relación 'tecnico' a este esquema
    tecnico: Optional[TecnicoInfo] = None 

    @root_validator(pre=True)
    def extraer_datos_virtuales(cls, obj):
        # Si es un objeto de SQLAlchemy, lo convertimos a dict para no romper nada
        if not isinstance(obj, dict):
            usuario = getattr(obj, "usuario", None)
            tel = "No disponible"
            if usuario:
                tel = getattr(usuario, "telefono", "No disponible") or "No disponible"
            
            # Creamos un diccionario con la data real de la tabla
            data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            data["telefono_cliente"] = tel
            data["tecnico"] = getattr(obj, "tecnico", None)
            return data
        return obj