from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.usuario import Usuario # 👈 Ya lo importas aquí
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
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        taller_override = payload.get("taller_id")
        rol_override = payload.get("rol_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No se pudo validar el usuario: sub faltante",
            )
    except JWTError as e:
        print(f"❌ ERROR JWT DETALLADO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Token inválido: {str(e)}", 
        )
    
    try:
        user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido en token")

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
    
    # Aplicar overrides en memoria para impersonación
    user.original_rol_id = user.rol_id
    if taller_override is not None:
        user.taller_id = int(taller_override)
    if rol_override is not None:
        user.rol_id = int(rol_override)

    return user

# --- CANDADOS DE SEGURIDAD ---

def get_current_active_user(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    original_rol_id = getattr(current_user, "original_rol_id", current_user.rol_id)
    if original_rol_id in (1, 3) and current_user.taller_id:
        from app.models.taller import Taller
        taller = db.query(Taller).filter(Taller.id == current_user.taller_id).first()
        if not taller or not taller.estado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso restringido: El taller se encuentra inhabilitado.",
            )

    return current_user

def get_current_admin_taller(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user), # 👈 Encadenamos con el validador de activo
) -> Usuario:
    """Candado: Solo permite el paso a Administradores de Taller (Web)"""
    if current_user.rol_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requieren permisos de Administrador de Taller.",
        )

    if not current_user.taller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: El usuario no tiene un taller asignado.",
        )

    from app.models.taller import Taller
    taller = db.query(Taller).filter(Taller.id == current_user.taller_id).first()
    if not taller or not taller.estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido: El taller se encuentra inhabilitado.",
        )

    return current_user

def get_current_cliente(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    """Candado: Solo permite el paso a Clientes (Móvil)"""
    if current_user.rol_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Endpoint exclusivo para la aplicación móvil.",
        )
    return current_user

def get_current_superadmin(
    current_user: Usuario = Depends(get_current_active_user),
) -> Usuario:
    """Candado: Solo permite el paso a Super Administradores de la Plataforma"""
    # Verificamos si su rol original en base de datos es 4 (Super Administrador)
    original_rol_id = getattr(current_user, "original_rol_id", current_user.rol_id)
    if original_rol_id != 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requieren permisos de Super Administrador.",
        )
    return current_user
