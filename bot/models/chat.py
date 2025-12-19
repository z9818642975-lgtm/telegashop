from __future__ import annotations
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    operator_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    order_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("orders.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    admin_requested_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    admin_joined_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    admin_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
