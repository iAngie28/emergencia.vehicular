from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from decimal import Decimal
from datetime import time, datetime

# Importar schema de horarios para reutilización
class HorarioTallerInfo(BaseModel):
    id: int
    dia: str
    hora_apertura: time
    hora_cierre: time
    
    class Config:
        from_attributes = True

class TallerBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)
    ciudad: Optional[str] = Field(None, max_length=100)
    # Validamos que las coordenadas sean reales (Bolivia está en estos rangos aprox)
    latitud: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitud: Optional[Decimal] = Field(None, ge=-180, le=180)
    estado: bool = True
    telefono: Optional[str] = None 
    comision_porcentaje: Optional[float] = None
    stripe_account_id: Optional[str] = None
    plan_suscripcion: Optional[str] = "gratuito"
    suscripcion_expira: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    tipo_inhabilitacion: Optional[str] = None
    motivo_inhabilitacion: Optional[str] = None
    fecha_inhabilitacion: Optional[datetime] = None
    inhabilitado_por_usuario_id: Optional[int] = None

class TallerCreate(TallerBase):
    pass

class TallerUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    telefono: Optional[str] = None
    estado: Optional[bool] = True
    comision_porcentaje: Optional[float] = 10.0
    stripe_account_id: Optional[str] = None
    plan_suscripcion: Optional[str] = "gratuito"
    suscripcion_expira: Optional[datetime] = None
    stripe_subscription_id: Optional[str] = None
    tipo_inhabilitacion: Optional[str] = None
    motivo_inhabilitacion: Optional[str] = None
    fecha_inhabilitacion: Optional[datetime] = None
    inhabilitado_por_usuario_id: Optional[int] = None

class Taller(TallerBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    cantidad_tecnicos: int = 0
    especialidades_activas: List[str] = []
    horarios: List[HorarioTallerInfo] = []
    esta_abierto_ahora: bool = False

    class Config:
        from_attributes = True


# Tarjeta del Directorio de Talleres (solo consulta, app móvil del cliente)
class TallerDirectorioOut(BaseModel):
    id: int
    nombre: str
    especialidad: str
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    calificacion_promedio: Optional[float] = None
    especialidades_activas: List[str] = []
    esta_abierto_ahora: bool = False
    distancia_km: Optional[float] = None
    imagen_url: Optional[str] = None


class TallerTecnicoResumen(BaseModel):
    id: int
    nombre: str
    apellido: Optional[str] = None
    correo: str
    telefono: Optional[str] = None
    esta_activo: bool = True
    especialidades: List[str] = []


class TallerReporteResumen(BaseModel):
    id: int
    incidente_id: int
    tipo_reporte: str
    motivo: str
    descripcion: str
    estado: str
    fecha_creacion: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None
    tecnico_id: Optional[int] = None
    tecnico_nombre: Optional[str] = None


class TallerEmergenciaResumen(BaseModel):
    id: int
    estado: str
    prioridad: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    pago_estado: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    tecnico_id: Optional[int] = None
    tecnico_nombre: Optional[str] = None
    cliente_nombre: Optional[str] = None


class TallerDetalleSuperadmin(BaseModel):
    taller: Taller
    estado_habilitacion: bool
    tecnicos: List[TallerTecnicoResumen] = []
    reportes: List[TallerReporteResumen] = []
    emergencias: List[TallerEmergenciaResumen] = []


class TallerInhabilitarRequest(BaseModel):
    motivo: str = Field(..., min_length=5, max_length=500)
    tipo_inhabilitacion: Literal["temporal", "permanente"] = "temporal"
