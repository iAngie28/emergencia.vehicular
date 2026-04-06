from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Pago(Base):
    id = Column(Integer, primary_key=True, index=True)
    incidente_id = Column(
        Integer, 
        ForeignKey("incidente.id", ondelete="RESTRICT"), 
        nullable=False
    )
    
    # Bloqueamos el borrado de usuarios/talleres con pagos pendientes o realizados
    usuario_id = Column(
        Integer, 
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False # Un pago siempre tiene un emisor
    )
    
    taller_id = Column(
        Integer, 
        ForeignKey("taller.id", ondelete="RESTRICT"),
        nullable=False # Un pago siempre tiene un receptor
    )
    
    monto = Column(Numeric(10, 2), nullable=False)
    comision_plataforma = Column(Numeric(10, 2)) # El 10%
    metodo_pago = Column(String(50)) # 'qr', 'transferencia'
    estado = Column(String(20), default="pendiente")
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    incidente = relationship("Incidente", back_populates="pagos")
    usuario = relationship("Usuario", back_populates="pagos")
    taller = relationship("Taller", back_populates="pagos")