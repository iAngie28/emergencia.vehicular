from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Evidencia(Base):
    __tablename__ = "evidencia"
    id = Column(Integer, primary_key=True, index=True)
    
    # LA LLAVE FORÁNEA: Conecta esta foto/audio con su incidente
    incidente_id = Column(
    Integer, 
    ForeignKey("incidente.id", ondelete="CASCADE"), # <--- Limpieza automática
    nullable=False
    )
    
    tipo_archivo = Column(String(20)) # 'imagen', 'audio'
    url_archivo = Column(String(255)) # Ruta en el servidor/S3
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    # Conexión inversa para Python
    incidente = relationship("Incidente", back_populates="evidencias")