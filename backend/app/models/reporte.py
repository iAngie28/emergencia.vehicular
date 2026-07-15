from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Reporte(Base):
    __tablename__ = "reporte"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    incidente_id = Column(
        Integer, 
        ForeignKey("incidente.id", ondelete="RESTRICT"), 
        nullable=False,
        unique=True,  # Restricción: un único reporte por incidente
        index=True
    )
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    tecnico_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="SET NULL"), 
        nullable=True,
        index=True
    )
    tipo_reporte = Column(String(20), nullable=False)  # 'taller' o 'tecnico'
    motivo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String(20), default="abierto")  # 'abierto', 'en_revision', 'resuelto'
    respuesta = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_resolucion = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="reportes_creados")
    tecnico = relationship("Usuario", foreign_keys=[tecnico_id], back_populates="reportes_recibidos")
    incidente = relationship("Incidente", back_populates="reportes")
    taller = relationship("Taller", back_populates="reportes")
