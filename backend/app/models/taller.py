from sqlalchemy import Column, Integer, String, Float, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.usuario import Especialidad
class Taller(Base):
    __tablename__ = "taller"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    telefono = Column(String(20))
    estado = Column(Boolean, default=True) # Activo o Inactivo
    comision_porcentaje = Column(Float, default=10.0) # Tu ganancia [Audio]

    # Relaciones
    usuarios = relationship("Usuario", back_populates="taller")
    horarios = relationship("HorarioTaller", back_populates="taller")
    incidentes = relationship("Incidente", back_populates="taller")
    pagos = relationship("Pago", back_populates="taller")
    bitacoras = relationship("Bitacora", back_populates="taller")


    @property
    def especialidades_activas(self):
        servicios = set()
        for u in self.usuarios:
            # Si es Técnico (Rol 3) y está activo
            if u.rol_id == 3 and u.esta_activo:
                for esp in u.especialidades:
                    servicios.add(esp.nombre)
        return sorted(list(servicios))