from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.usuario import Usuario 
from app.core.config import settings 

# Este es el endpoint donde el usuario pide el token
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(reusable_oauth2)
) -> Usuario:
    # --- MODO QA DEBUG ---
    print(f"🕵️‍♂️ QA Backend -> Token recibido (primeros 15 chars): {token[:15]}...")
    
    try:
        # Decodificamos el token usando la configuración global
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No se pudo validar el usuario: sub faltante",
            )
    except JWTError as e:
        # --- MODO QA DEBUG ---
        print(f"❌ ERROR JWT DETALLADO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            # Ahora el error en Angular te dirá exactamente por qué falló
            detail=f"Token inválido: {str(e)}", 
        )
    
    # Buscamos el usuario asegurando que el ID sea entero
    try:
        user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido en token")

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
    
    return user


def get_current_admin_taller(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Candado: Solo permite el paso a Administradores de Taller (Web)"""
    if current_user.rol_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requieren permisos de Administrador de Taller.",
        )
    return current_user

def get_current_cliente(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Candado: Solo permite el paso a Clientes (Móvil)"""
    if current_user.rol_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Endpoint exclusivo para la aplicación móvil.",
        )
    return current_user