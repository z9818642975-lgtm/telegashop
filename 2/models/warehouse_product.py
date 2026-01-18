# bot/models/warehouse_product.py
from __future__ import annotations

# bot/models/warehouse_product.py
from __future__ import annotations





from sqlalchemy import Integer, ForeignKey


from sqlalchemy.orm import Mapped, mapped_column





from bot.models.base import Base








class WarehouseProduct(Base):


    __tablename__ = "warehouse_products"





    id: Mapped[int] = mapped_column(


        primary_key=True,


        autoincrement=True,


    )





    warehouse_id: Mapped[int] = mapped_column(


        ForeignKey("warehouses.id", ondelete="CASCADE"),


        index=True,


        nullable=False,


    )





    product_id: Mapped[int] = mapped_column(


        ForeignKey("products.id", ondelete="CASCADE"),


        index=True,


        nullable=False,


    )





    qty_available: Mapped[int] = mapped_column(


        Integer,


        nullable=False,


        default=0,


    )





