from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class TokenDispositivo(Base):
    __tablename__ = "token_dispositivo"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="CASCADE"), 
        nullable=False
    )
    token_fcm = Column(Text, nullable=False)
    plataforma = Column(String(20)) # 'android', 'ios', 'web'
    ultima_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="tokens")

class Notificacion(Base):
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="CASCADE"), 
        nullable=False
    )
    incidente_id = Column(
        Integer, 
        ForeignKey("incidente.id", ondelete="SET NULL"), 
        nullable=True
    )
    titulo = Column(String(100))
    mensaje = Column(Text)
    tipo = Column(String(50)) # 'emergencia', 'pago', 'sistema'
    leido = Column(Boolean, default=False)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())
    
    usuario = relationship("Usuario", back_populates="notificaciones")
    incidente = relationship("Incidente", back_populates="notificaciones")