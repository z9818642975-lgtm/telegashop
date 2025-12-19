from __future__ import annotations
from sqlalchemy import Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), unique=True)
    proof_file_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed_by_operator_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confirmed_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
