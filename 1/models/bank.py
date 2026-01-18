# bot/models/bank.py

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class Bank(Base):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Bank id={self.id} name={self.name}>"

