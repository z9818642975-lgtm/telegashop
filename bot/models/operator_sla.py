from __future__ import annotations
from sqlalchemy import Integer, Date, Float
from sqlalchemy.orm import Mapped, mapped_column
from bot.core.db import Base

class OperatorSLAStat(Base):
    __tablename__ = "operator_sla_stats"
    operator_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(Date, primary_key=True)
    orders_done: Mapped[int] = mapped_column(Integer, default=0)
    auto_closed_shifts: Mapped[int] = mapped_column(Integer, default=0)
    reassignments: Mapped[int] = mapped_column(Integer, default=0)
    avg_response_sec: Mapped[float] = mapped_column(Float, default=0.0)
    warnings_count: Mapped[int] = mapped_column(Integer, default=0)
