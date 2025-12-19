from __future__ import annotations
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from bot.core.db import Base

class WarehouseProduct(Base):
    __tablename__ = "warehouse_products"
    warehouse_id: Mapped[int] = mapped_column(Integer, ForeignKey("warehouses.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), primary_key=True)
    qty_available: Mapped[int] = mapped_column(Integer, default=0)
    low_notified: Mapped[bool] = mapped_column(Boolean, default=False)
