# bot/models/user.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.models.enums import UserRole

if TYPE_CHECKING:
    from .order import Order
    from .user import User


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="userrole"),
        nullable=False,
        server_default=UserRole.CLIENT,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("now()"),
        nullable=False,
    )

    # ==========================
    # RELATIONS
    # ==========================

    # Заказы, где пользователь — КЛИЕНТ
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        foreign_keys="Order.client_id",
        back_populates="client",
        lazy="selectin",
    )

    # Заказы, где пользователь — ОПЕРАТОР
    operated_orders: Mapped[list["Order"]] = relationship(
        "Order",
        foreign_keys="Order.operator_id",
        lazy="selectin",
        overlaps="client,orders,operator",
    )
# noqa: F821
