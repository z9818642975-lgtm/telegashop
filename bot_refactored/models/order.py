from __future__ import annotations

from enum import Enum
from datetime import datetime

from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot_refactored.db import Base


class OrderStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    WAITING_CONFIRMATION = "waiting_confirmation"
    PAID = "paid"
    DONE = "done"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    shift_id: Mapped[int | None] = mapped_column(
        ForeignKey("operator_shifts.id"),
        nullable=True,
        index=True,
    )

    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.NEW,
    )

    # timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    paid_at: Mapped[datetime | None]
    completed_at: Mapped[datetime | None]

    # payment proof (human-in-the-loop)
    payment_photo_id: Mapped[str | None]
    payment_comment: Mapped[str | None]

