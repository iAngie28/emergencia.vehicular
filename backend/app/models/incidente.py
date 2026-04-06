from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Incidente(Base):
    __tablename__ = "incidente" # Recomendado forzar el nombre

    id = Column(Integer, primary_key=True, index=True)
    
    # --- LLAVES FORÁNEAS ---
    # Un incidente NO puede quedar huérfano de vehículo o usuario
    vehiculo_id = Column(
        Integer, 
        ForeignKey("vehiculo.id", ondelete="RESTRICT"), 
        nullable=False
    )

    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="RESTRICT"), 
        nullable=False
    )

# Si el taller desaparece, el incidente queda libre para otro (SET NULL)
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="SET NULL"), 
        nullable=True
    )
    # --- DATOS DE UBICACIÓN Y ESTADO ---
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    prioridad = Column(String(20)) # 'baja', 'media', 'alta'
    estado = Column(String(20), default="pendiente") # 'pendiente', 'en_proceso', 'atendido'
    
    # --- CAMPOS PARA LA IA (Core del proyecto) ---
    transcripcion_audio = Column(Text)
    clasificacion_ia = Column(String(100)) # (Nota: quité la tilde para evitar líos de encoding)
    resumen_ia = Column(Text)

    # --- RELACIONES (Bidireccionales) ---
    # Para saber qué auto es: incidente.vehiculo.marca
    vehiculo = relationship("Vehiculo", back_populates="incidentes")
    
    # Para saber quién es el cliente: incidente.usuario.nombre
    usuario = relationship("Usuario", back_populates="incidentes")
    
    # Para saber qué taller lo atiende: incidente.taller.nombre
    taller = relationship("Taller", back_populates="incidentes")
    
    # Para ver las fotos/audios: incidente.evidencias
    evidencias = relationship("Evidencia", back_populates="incidente", cascade="all, delete-orphan")
    # Relación con Pagos (Un incidente puede generar un pago)
    pagos = relationship("Pago", back_populates="incidente", uselist=False, cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="incidente")