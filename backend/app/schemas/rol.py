from pydantic import BaseModel, Field
from typing import Optional

class RolBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50) # 'admin', 'taller', 'cliente'

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    nombre: Optional[str] = None

class Rol(RolBase):
    id: int

    class Config:
        from_attributes = True