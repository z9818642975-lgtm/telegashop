# bot/models/user.py
from __future__ import annotations

# bot/models/user.py
from __future__ import annotations





from datetime import datetime





from sqlalchemy import BigInteger, String, DateTime, Boolean, Enum


from sqlalchemy.orm import Mapped, mapped_column





from bot.db.base import Base   # ✅ ВАЖНО


from bot.models.enums import UserRole








class User(Base):


    __tablename__ = "users"





    id: Mapped[int] = mapped_column(


        BigInteger,


        primary_key=True,


        autoincrement=True,


    )





    tg_id: Mapped[int] = mapped_column(


        BigInteger,


        unique=True,


        nullable=False,


        index=True,


    )





    role: Mapped[UserRole] = mapped_column(


        Enum(UserRole),


        nullable=False,


        default=UserRole.CLIENT,


    )





    username: Mapped[str | None] = mapped_column(


        String(255),


        nullable=True,


    )





    full_name: Mapped[str | None] = mapped_column(


        String(255),


        nullable=True,


    )





    is_active: Mapped[bool] = mapped_column(


        Boolean,


        default=True,


        nullable=False,


    )





    created_at: Mapped[datetime] = mapped_column(


        DateTime(timezone=True),


        default=datetime.utcnow,


        nullable=False,


    )





