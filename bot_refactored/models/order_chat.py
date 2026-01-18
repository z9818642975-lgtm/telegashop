from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from bot_refactored.db import Base

class OrderChatMessage(Base):
    __tablename__ = "order_chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    sender_id: Mapped[int]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

