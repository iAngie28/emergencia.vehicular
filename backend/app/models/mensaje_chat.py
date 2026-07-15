from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MensajeChat(Base):
    __tablename__ = "mensaje_chat"

    id = Column(Integer, primary_key=True, index=True)
    incidente_id = Column(
        Integer, 
        ForeignKey("incidente.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    remitente_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="CASCADE"), 
        nullable=False
    )
    contenido = Column(Text, nullable=False)
    tipo = Column(String(20), default="texto")  # 'texto', 'imagen'
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    incidente = relationship("Incidente", back_populates="mensajes_chat")
    remitente = relationship("Usuario", back_populates="mensajes_chat")
