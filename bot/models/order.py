from __future__ import annotations
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    operator_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    shift_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("operator_shifts.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, index=True, default="NEW")
    delivery_method: Mapped[str] = mapped_column(String)  # COURIER / PICKUP
    pickup_address_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    bank_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bank_account_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("bank_accounts.id"), nullable=True)
    delivery_fee: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
