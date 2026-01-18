from __future__ import annotations

import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from bot.db.base import Base
from bot.models.enums import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )



    status: Mapped[OrderStatus] = mapped_column(
        String(32),
        nullable=False,
        default=OrderStatus.NEW,
    )

    # ============================
    # DELIVERY
    # ============================

    delivery_type: Mapped[str] = mapped_column(
        String(16),  # pickup | delivery
        nullable=False,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ============================
    # OPERATOR → CLIENT (PICKUP)
    # ============================

    pickup_comment: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    pickup_photo_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    ready_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ============================
    # META
    # ============================

    total_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    # ============================
    # RELATIONS
    # ============================

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
    )

