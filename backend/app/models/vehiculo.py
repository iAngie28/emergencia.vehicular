from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Vehiculo(Base):
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), unique=True, index=True, nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))
    anio = Column(Integer)
    color = Column(String(30))
    tipo_combustible = Column(String(30))
    detalle = Column(Text)
    
    # FK: A quién le pertenece el auto
    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="RESTRICT"), 
        nullable=False
    )
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="vehiculos")
    incidentes = relationship(
        "Incidente", 
        back_populates="vehiculo",
        cascade="all, delete-orphan" # Solo si quieres borrar incidentes al borrar el auto
    )