from sqlalchemy import Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    base_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    min_qty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # 🔒 КАНОНИЧЕСКИЙ АЛИАС
    @property
    def price(self) -> int:
        return self.base_price
