from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class EvidenciaBase(BaseModel):
    incidente_id: int
    tipo_archivo: str  # 'imagen' o 'audio'
    url_archivo: str   # Usamos str para rutas locales o S3

class EvidenciaCreate(EvidenciaBase):
    pass

class EvidenciaUpdate(EvidenciaBase):
    incidente_id: Optional[int] = None
    tipo_archivo: Optional[str] = None
    url_archivo: Optional[str] = None

class Evidencia(EvidenciaBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True