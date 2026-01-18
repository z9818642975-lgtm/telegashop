from __future__ import annotations

import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base


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
