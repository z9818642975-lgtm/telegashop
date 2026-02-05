# bot/models/order_item.py
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.models.enums import OrderItemStatus

if TYPE_CHECKING:
    from .order_item import OrderItem


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    status: Mapped[OrderItemStatus] = mapped_column(
        Enum(OrderItemStatus, name="orderitemstatus"),
        nullable=False,
        default=OrderItemStatus.NEW,
    )

    accepted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    paid_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)

    # =========================
    # RELATIONS
    # =========================

    order = relationship(
        "Order",
        back_populates="items",
    )

    product = relationship(
        "Product",
        lazy="joined",
    )

    operator = relationship(
        "User",
        foreign_keys=[operator_id],
        lazy="joined",
    )
# noqa: F821
