from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt # Asegúrate de tener 'python-jose' en tu requirements
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash_clave(password: str) -> str:
    return pwd_context.hash(password)

def verificar_clave(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- AGREGA ESTA FUNCIÓN PARA EL LOGIN ---
def crear_token_acceso(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt