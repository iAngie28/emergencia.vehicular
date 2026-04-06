from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Bitacora(Base):
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=True) # Quién hizo el cambio
    tabla = Column(String(50)) # 'incidente', 'usuario', 'pago'
    tabla_id = Column(Integer) # El ID del registro afectado
    accion = Column(String(20)) # 'crear', 'actualizar', 'eliminar'
    
    # Auditoría JSON
    valor_anterior = Column(JSON, nullable=True)
    valor_nuevo = Column(JSON, nullable=True)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())


    usuario = relationship("Usuario", back_populates="bitacoras")