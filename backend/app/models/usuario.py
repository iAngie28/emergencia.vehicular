from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.base_class import Base

class Usuario(Base):
    __tablename__ = "usuario" # Forzamos el nombre en minúscula por si acaso

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    clave_hash = Column(String, nullable=False)
    telefono = Column(String(20), nullable=True)

    # --- LLAVES FORÁNEAS (Físicas en la DB) ---
    rol_id = Column(
        Integer, 
        ForeignKey("rol.id", ondelete="RESTRICT"), 
        nullable=False
    )
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="SET NULL"), 
        nullable=True
    )
    # --- RELACIONES INVERSAS (Navegación en Python) ---
    rol = relationship("Rol", back_populates="usuarios")
    taller = relationship("Taller", back_populates="usuarios")
    vehiculos = relationship("Vehiculo", back_populates="usuario", cascade="all, delete-orphan")
    incidentes = relationship("Incidente", back_populates="usuario")
    pagos = relationship("Pago", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario", cascade="all, delete-orphan")
    tokens = relationship("TokenDispositivo", back_populates="usuario", cascade="all, delete-orphan")
    bitacoras = relationship("Bitacora", back_populates="usuario")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expiracion = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)