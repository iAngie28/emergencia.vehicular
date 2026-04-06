from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Rol(Base):
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False) # 'admin', 'taller', 'cliente'
    
    # Relación inversa: Un rol tiene muchos usuarios
    usuarios = relationship(
        "Usuario", 
        back_populates="rol",
        passive_deletes=True 
    )