# bot/models/operator_shift.py
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base

if TYPE_CHECKING:
    pass


class OperatorShift(Base):
    __tablename__ = "operator_shifts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # 🔑 ВСЕГДА tg_id
    operator_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.tg_id"),
        nullable=False,
        index=True,
    )

    pickup_address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(DateTime)

    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime)

    warned_15: Mapped[bool] = mapped_column(Boolean, default=False)
    warned_17: Mapped[bool] = mapped_column(Boolean, default=False)
    warned_20: Mapped[bool] = mapped_column(Boolean, default=False)

    auto_closed: Mapped[bool] = mapped_column(Boolean, default=False)

    # relationship нужен watcher'у
    operator = relationship(
        "User",
        primaryjoin="OperatorShift.operator_id == User.tg_id",
        viewonly=True,
    )
# noqa: F821
