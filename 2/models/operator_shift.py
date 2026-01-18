from __future__ import annotations

import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class OperatorShift(Base):
    __tablename__ = "operator_shifts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    operator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # 📍 Адрес самовывоза (обязателен)
    pickup_address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    ended_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_activity_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # ⏱ предупреждения
    warned_15: Mapped[bool] = mapped_column(Boolean, default=False)
    warned_17: Mapped[bool] = mapped_column(Boolean, default=False)
    warned_20: Mapped[bool] = mapped_column(Boolean, default=False)

