from sqlalchemy import Column, Integer, String, ForeignKey, Time, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

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

class Especialidad(Base):
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True)
    descripcion = Column(Text)
    
    talleres = relationship("TallerEspecialidad", back_populates="especialidad")

class TallerEspecialidad(Base):
    __tablename__ = "taller_especialidad"
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="CASCADE"), 
        primary_key=True
    )
    especialidad_id = Column(
        Integer, 
        ForeignKey("especialidad.id", ondelete="CASCADE"), 
        primary_key=True
    )
    nivel_experiencia = Column(String(50)) # 'basico', 'experto'

    taller = relationship("Taller", back_populates="especialidades")
    especialidad = relationship("Especialidad", back_populates="talleres")