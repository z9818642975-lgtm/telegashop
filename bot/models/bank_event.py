from __future__ import annotations
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class BankEvent(Base):
    __tablename__ = "bank_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(Integer, index=True)
    bank_account_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    event_type: Mapped[str] = mapped_column(String)  # SHOWN/PAID/TIMEOUT
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
