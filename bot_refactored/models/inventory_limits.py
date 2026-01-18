from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base

class InventoryLimit(Base):
    __tablename__ = "inventory_limits"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    min_qty: Mapped[int] = mapped_column(default=0)

