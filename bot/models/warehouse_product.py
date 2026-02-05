# bot/models/warehouse_product.py
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base

if TYPE_CHECKING:
    pass


class WarehouseProduct(Base):
    __tablename__ = "warehouse_products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey("warehouses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    qty_available: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
# noqa: F821
