from app.crud.base import CRUDBase
from app.models.mensaje_chat import MensajeChat
from app.schemas.mensaje_chat import MensajeChatCreate
from sqlalchemy.orm import Session
from typing import List

class CRUDMensajeChat(CRUDBase[MensajeChat, MensajeChatCreate, MensajeChatCreate]):
    def obtener_por_incidente(self, db: Session, *, incidente_id: int) -> List[MensajeChat]:
        return (
            db.query(self.model)
            .filter(self.model.incidente_id == incidente_id)
            .order_by(self.model.fecha_envio.asc())
            .all()
        )

mensaje_chat_crud = CRUDMensajeChat(MensajeChat)
