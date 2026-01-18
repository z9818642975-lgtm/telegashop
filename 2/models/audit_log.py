# bot/models/audit_log.py
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    actor_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    entity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    entity_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

