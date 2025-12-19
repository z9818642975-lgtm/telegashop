from __future__ import annotations
from sqlalchemy import Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class OperatorShift(Base):
    __tablename__ = "operator_shifts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    pickup_address: Mapped[str] = mapped_column(Text)
    started_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    ended_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    auto_closed: Mapped[bool] = mapped_column(Boolean, default=False)
