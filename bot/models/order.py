# bot/models/order.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.models.enums import OrderStatus

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .payment import Payment
    from .user import User


class Order(Base):
    __tablename__ = "orders"

    # ==========================
    # BASE
    # ==========================

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    # ==========================
    # STATE
    # ==========================

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="orderstatus"),
        nullable=False,
        index=True,
        default=OrderStatus.CART,
    )

    total_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # ==========================
    # PICKUP (CLIENT FSM)
    # ==========================

    pickup_comment: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    pickup_photo_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # ==========================
    # PAYMENT (CHEQUE META)
    # ==========================

    payment_proof_file_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    payment_proof_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    payment_submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    payment_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ==========================
    # SLA / LIFECYCLE
    # ==========================

    sla_deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ==========================
    # TIMESTAMPS
    # ==========================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("now()"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ==========================
    # RELATIONS
    # ==========================

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    client: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="orders",
        lazy="joined",
        overlaps="operated_orders",
    )

    operator: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[operator_id],
        viewonly=True,                 # ← КЛЮЧЕВО
        lazy="joined",
        overlaps="orders,operated_orders",
    )


    payment: Mapped["Payment | None"] = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="joined",
    )
# noqa: F821
