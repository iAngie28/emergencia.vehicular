from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base import Base
from app.crud.crud_bitacora import bitacora_crud

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, usuario_id: Optional[int] = None) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        bitacora_crud.registrar(
            db,
            usuario_id=usuario_id,
            tabla=self.model.__tablename__,
            accion="crear",
            nuevo=obj_in_data
        )
        return db_obj

    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: ModelType, 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        usuario_id: Optional[int] = None
    ) -> ModelType:
        # 1. Obtenemos los datos actuales antes de cambiar nada (JSONable para la bitácora)
        obj_data = jsonable_encoder(db_obj)
        
        # 2. Preparamos los datos que vienen del esquema o diccionario
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True) # Ignora campos no enviados

        # 3. Aplicamos los cambios al objeto de la base de datos
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # 4. Registramos el cambio con "antes" y "después"
        bitacora_crud.registrar(
            db,
            usuario_id=usuario_id,
            tabla=self.model.__tablename__,
            accion="actualizar",
            anterior=obj_data,
            nuevo=update_data
        )
        return db_obj

    def remove(self, db: Session, *, id: int, usuario_id: Optional[int] = None) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj:
            datos_eliminados = jsonable_encoder(obj)
            db.delete(obj)
            db.commit()
            bitacora_crud.registrar(
                db,
                usuario_id=usuario_id,
                tabla=self.model.__tablename__,
                accion="eliminar",
                anterior=datos_eliminados
            )
        return obj