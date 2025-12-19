from __future__ import annotations
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class RestockOrder(Base):
    __tablename__ = "restock_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, index=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, index=True)
    qty: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="CREATED")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
