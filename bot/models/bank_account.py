# bot/models/bank_account.py
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base

if TYPE_CHECKING:
    pass


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    bank_name: Mapped[str] = mapped_column(String, nullable=False)

    card_number: Mapped[str | None] = mapped_column(String, nullable=True)
    card_masked: Mapped[str | None] = mapped_column(String, nullable=True)

    sbp_phone: Mapped[str | None] = mapped_column(String, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    disabled_until: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    load: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )


# noqa: F821
