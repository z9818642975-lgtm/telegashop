# bot/models/warehouse.py
from sqlalchemy import Integer, String, Boolean, ForeignKey

# bot/models/warehouse.py
from sqlalchemy import Integer, String, Boolean, ForeignKey


from sqlalchemy.orm import Mapped, mapped_column





from bot.db.base import Base








class Warehouse(Base):


    __tablename__ = "warehouses"





    id: Mapped[int] = mapped_column(


        Integer,


        primary_key=True,


    )





    title: Mapped[str] = mapped_column(


        String,


        unique=True,


        nullable=False,


    )





    address: Mapped[str] = mapped_column(


        String,


        nullable=False,


    )





    owner_id: Mapped[int] = mapped_column(


        ForeignKey("users.id", ondelete="CASCADE"),


        nullable=False,


    )





    is_active: Mapped[bool] = mapped_column(


        Boolean,


        default=True,


        nullable=False,


    )





