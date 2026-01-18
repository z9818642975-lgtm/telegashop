from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base


class InventoryItem(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)

    quantity: Mapped[int] = mapped_column(default=0)
    reserved: Mapped[int] = mapped_column(default=0)

