# -*- coding: utf-8 -*-
# bot/models/order_item.py
# bot/models/order_item.py


from __future__ import annotations





import datetime





from sqlalchemy import (


    Integer,


    ForeignKey,


    DateTime,


    Enum,


)


from sqlalchemy.orm import Mapped, mapped_column, relationship





from bot.db.base import Base


from bot.models.enums import OrderItemStatus








class OrderItem(Base):


    __tablename__ = "order_items"





    id: Mapped[int] = mapped_column(


        Integer,


        primary_key=True,


        autoincrement=True,


    )





    order_id: Mapped[int] = mapped_column(


        ForeignKey("orders.id", ondelete="CASCADE"),


        nullable=False,


        index=True,


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





    price: Mapped[int] = mapped_column(


        Integer,


        nullable=False,


        default=0,


    )





    status: Mapped[OrderItemStatus] = mapped_column(


        Enum(


            OrderItemStatus,


            name="orderitemstatus",


            native_enum=True,


        ),


        nullable=False,


        default=OrderItemStatus.NEW,


    )





    completed_at: Mapped[datetime.datetime | None] = mapped_column(


        DateTime,


        nullable=True,


    )





    # relationships


    order: Mapped["Order"] = relationship(


        "Order",


        back_populates="items",


    )





    product: Mapped["Product"] = relationship(


        "Product",


        lazy="joined",


    )





