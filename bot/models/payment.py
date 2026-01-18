from __future__ import annotations

from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.models.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    # ============================
    # RELATIONS
    # ============================

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment",
        lazy="selectin",
    )

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id"),
        nullable=False,
    )

    bank_account = relationship(
        "BankAccount",
        lazy="joined",
    )

    # ============================
    # PAYMENT DATA
    # ============================

    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="paymentmethod"),
        nullable=False,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="paymentstatus"),
        nullable=False,
        default=PaymentStatus.NEW,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    requisites: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    check_file_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    reject_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ============================
    # TIMESTAMPS
    # ============================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    rejected_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

