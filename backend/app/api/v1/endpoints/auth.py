from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.crud.crud_usuario import usuario_crud
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # 1. Verificar si el usuario existe y la clave es correcta
    usuario = usuario_crud.authenticate(
        db, correo=form_data.username, clave=form_data.password
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo o contraseña incorrectos",
        )
    
    # 2. Generar el Token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.crear_token_acceso(
            usuario.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }