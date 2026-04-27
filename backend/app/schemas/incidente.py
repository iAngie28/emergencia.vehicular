from pydantic import BaseModel, Field, root_validator
from typing import Optional, Dict, Any
from decimal import Decimal
from datetime import datetime

# Esquema para mostrar info básica del técnico
class TecnicoInfo(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

# Esquema para mostrar info del vehículo
class VehiculoInfo(BaseModel):
    id: int
    placa: str
    marca: str
    modelo: str
    class Config:
        from_attributes = True

# Esquema para mostrar info del pago asociado
class PagoInfo(BaseModel):
    id: int
    monto: Decimal
    comision_plataforma: Decimal
    estado: str
    class Config:
        from_attributes = True

# Esquema para mostrar info básica del taller
class TallerInfo(BaseModel):
    id: int
    latitud: Decimal
    longitud: Decimal
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
    fecha_creacion: Optional[datetime] = None

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
    vehiculo: Optional[VehiculoInfo] = None  # 🚗 Relación con el vehículo
    pagos: Optional[PagoInfo] = None  # Relación con el pago asociado
    taller: Optional[TallerInfo] = None  # Relación con el taller
    distancia_metros: Optional[float] = None  # 📏 Distancia al taller en metros 

    @root_validator(pre=True)
    def extraer_datos_virtuales(cls, obj):
        if not isinstance(obj, dict):
            usuario = getattr(obj, "usuario", None)
            tel = "No disponible"
            if usuario:
                tel = getattr(usuario, "telefono", "No disponible") or "No disponible"
            
            return {
                "id": obj.id,
                "vehiculo_id": obj.vehiculo_id,
                "usuario_id": obj.usuario_id,
                "taller_id": obj.taller_id,
                "tecnico_id": obj.tecnico_id,
                "latitud": obj.latitud,
                "longitud": obj.longitud,
                "prioridad": obj.prioridad,
                "estado": obj.estado,
                "pago_estado": obj.pago_estado,
                "telefono_cliente": tel,
                "motivo_cancelacion": obj.motivo_cancelacion,
                "transcripcion_audio": obj.transcripcion_audio,
                "clasificacion_ia": obj.clasificacion_ia,
                "resumen_ia": obj.resumen_ia,
                "fecha_creacion": obj.fecha_creacion,
                "tecnico": obj.tecnico,
                "vehiculo": obj.vehiculo,  # 🚗 Incluir relación con vehículo
                "pagos": obj.pagos,  # 🆕 Incluir relación con pagos
                "taller": obj.taller,  # 🆕 Incluir relación con taller
                "distancia_metros": getattr(obj, "distancia_metros", None)  # 📏 Incluir distancia
            }
        return obj