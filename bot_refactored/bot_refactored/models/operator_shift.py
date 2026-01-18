from __future__ import annotations

from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot_refactored.db import Base


class ShiftState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class OperatorShift(Base):
    __tablename__ = "operator_shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    state: Mapped[ShiftState] = mapped_column(
        SAEnum(ShiftState),
        default=ShiftState.CLOSED,
        nullable=False,
    )
    opened_at: Mapped[datetime | None]
    closed_at: Mapped[datetime | None]
    pickup_address: Mapped[str | None]

