from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from bot_refactored.db import Base

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

