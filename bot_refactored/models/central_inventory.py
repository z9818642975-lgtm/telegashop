from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base

class CentralInventory(Base):
    __tablename__ = "central_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(default=0)

