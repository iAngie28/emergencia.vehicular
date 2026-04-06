# app/db/base_class.py
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: any
    __name__: str
    
    # Genera el nombre de la tabla automáticamente a partir del nombre de la clase
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()