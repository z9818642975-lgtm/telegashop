# bot/models/warehouse_movement.py
from __future__ import annotations

# bot/models/warehouse_movement.py
from __future__ import annotations





from datetime import datetime





from sqlalchemy import Integer, ForeignKey, DateTime, String


from sqlalchemy.orm import Mapped, mapped_column





from bot.db.base import Base








class WarehouseMovement(Base):


    __tablename__ = "warehouse_movements"





    id: Mapped[int] = mapped_column(


        Integer,


        primary_key=True,


        autoincrement=True,


    )





    product_id: Mapped[int] = mapped_column(


        ForeignKey("products.id", ondelete="CASCADE"),


        nullable=False,


        index=True,


    )





    qty: Mapped[int] = mapped_column(


        Integer,


        nullable=False,


    )





    from_warehouse_id: Mapped[int | None] = mapped_column(


        ForeignKey("warehouses.id", ondelete="SET NULL"),


        nullable=True,


        index=True,


    )





    to_warehouse_id: Mapped[int | None] = mapped_column(


        ForeignKey("warehouses.id", ondelete="SET NULL"),


        nullable=True,


        index=True,


    )





    reason: Mapped[str] = mapped_column(


        String(255),


        nullable=False,


    )





    actor_id: Mapped[int | None] = mapped_column(


        Integer,


        nullable=True,


        index=True,


    )





    created_at: Mapped[datetime] = mapped_column(


        DateTime,


        default=datetime.utcnow,


        nullable=False,


    )





