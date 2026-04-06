from pydantic import BaseModel, Field
from typing import Optional

# 1. Campos comunes (Lo que siempre se comparte)
class VehiculoBase(BaseModel):
    placa: str = Field(..., min_length=6, max_length=15, description="Placa del vehículo")
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = Field(None, ge=1900, le=2027) # Validación de rango de año
    color: Optional[str] = None
    tipo_combustible: Optional[str] = None
    detalle: Optional[str] = None
    usuario_id: int # El dueño del auto

# 2. Schema para Crear (Igual al Base por ahora)
class VehiculoCreate(VehiculoBase):
    pass

# 3. Schema para Actualizar (Todo es opcional para permitir cambios parciales)
class VehiculoUpdate(VehiculoBase):
    placa: Optional[str] = None
    usuario_id: Optional[int] = None

# 4. Schema para Leer (Lo que el API responde)
class Vehiculo(VehiculoBase):
    id: int

    class Config:
        from_attributes = True # Esto es vital para que Pydantic lea de SQLAlchemy