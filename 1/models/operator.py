from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from bot.models.base import Base

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

