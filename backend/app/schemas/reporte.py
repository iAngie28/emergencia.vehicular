from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReporteBase(BaseModel):
    incidente_id: int = Field(..., description="ID del incidente asociado")
    tipo_reporte: str = Field(..., description="Tipo de reporte: 'taller' o 'tecnico'")
    motivo: str = Field(..., description="Motivo abreviado del reporte")
    descripcion: str = Field(..., description="Descripción detallada de la queja")

class ReporteCreate(ReporteBase):
    tecnico_id: Optional[int] = Field(None, description="ID del técnico si tipo_reporte es 'tecnico'")

class ReporteUpdate(BaseModel):
    respuesta: str = Field(..., description="Respuesta o descargo del administrador")
    estado: Optional[str] = Field("resuelto", description="Nuevo estado del reporte: 'resuelto' o 'en_revision'")

class ReporteOut(ReporteBase):
    id: int
    usuario_id: int
    taller_id: int
    tecnico_id: Optional[int]
    taller_nombre: Optional[str] = None
    tecnico_nombre: Optional[str] = None
    estado: str
    respuesta: Optional[str]
    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True
