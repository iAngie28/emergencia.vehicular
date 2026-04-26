from sqlalchemy import Column, Integer, String, ForeignKey, Time, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.usuario import Especialidad
# app/crud/crud_taller_detalles.py

class HorarioTaller(Base):
    __tablename__ = "horario_taller"
    id = Column(Integer, primary_key=True, index=True)
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="CASCADE"), 
        nullable=False
    )
    dia = Column(String(15)) # 'lunes', 'martes'...
    hora_apertura = Column(Time)
    hora_cierre = Column(Time)
    taller = relationship("Taller", back_populates="horarios")


