from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .taller import Taller
from app.schemas.taller import TallerCreate

# Base común: Lo que todos los estados del usuario comparten
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    correo: EmailStr
    rol_id: Optional[int] = None
    taller_id: Optional[int] = None
    taller: Optional[Taller] = None

# Registro: Incluye la clave (obligatoria y min 8 caracteres)
class UsuarioCreate(UsuarioBase):
    clave: str = Field(..., min_length=8)

# Actualización: Todo es Opcional para cambios parciales (PATCH)
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    correo: Optional[EmailStr] = None
    rol_id: Optional[int] = None
    taller_id: Optional[int] = None
    clave: Optional[str] = Field(None, min_length=8)

# Respuesta: Lo que enviamos al Frontend (Angular/Flutter)
class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

# Para el registro de "Dueño + Taller"
class RegistroSaaS(BaseModel):
    # Datos del Usuario
    nombre: str
    correo: EmailStr
    password: str
    # Datos de su nuevo Taller
    taller: TallerCreate

from pydantic import BaseModel, EmailStr

class RecuperarClaveRequest(BaseModel):
    correo: EmailStr

class RestablecerClaveInput(BaseModel):
    token: str
    nueva_clave: str