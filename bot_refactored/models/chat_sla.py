from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base


class ChatSLA(Base):
    __tablename__ = "chat_sla"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)

    last_client_msg_at: Mapped[datetime | None]
    last_operator_msg_at: Mapped[datetime | None]
    last_admin_msg_at: Mapped[datetime | None]

