from __future__ import annotations
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from bot.core.db import Base

class StockReservation(Base):
    __tablename__ = "stock_reservations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, ForeignKey("warehouses.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    qty: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="RESERVED")
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
