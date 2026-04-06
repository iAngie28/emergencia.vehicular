from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PagoBase(BaseModel):
    incidente_id: int
    usuario_id: int
    taller_id: int
    monto: Decimal = Field(..., max_digits=10, decimal_places=2)
    comision_plataforma: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    metodo_pago: str # 'qr', 'transferencia', 'tarjeta'
    estado: str = "pendiente"

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    estado: Optional[str] = None # Para pasar de 'pendiente' a 'completado'

class Pago(PagoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True