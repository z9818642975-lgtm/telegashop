from __future__ import annotations
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(Integer, index=True)
    bank_name: Mapped[str] = mapped_column(String, index=True)
    sbp_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    card_number: Mapped[str | None] = mapped_column(String, nullable=True)
    card_masked: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    load: Mapped[int] = mapped_column(Integer, default=0)
    weight: Mapped[int] = mapped_column(Integer, default=100)
    disabled_until: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
