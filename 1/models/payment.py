# bot/models/payment.py
from __future__ import annotations

# bot/models/payment.py
from __future__ import annotations





from datetime import datetime


from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum


from sqlalchemy.orm import Mapped, mapped_column, relationship





from bot.db.base import Base


from bot.models.enums import PaymentMethod, PaymentStatus








class Payment(Base):


    __tablename__ = "payments"





    id: Mapped[int] = mapped_column(Integer, primary_key=True)





    order_id: Mapped[int] = mapped_column(


        ForeignKey("orders.id", ondelete="CASCADE"),


        index=True,


        nullable=False,


    )





    # РІСљвЂ¦ Р вЂ™Р С›Р Сћ Р В­Р СћР С›Р вЂњР С› Р СњР вЂў Р ТђР вЂ™Р С’Р СћР С’Р вЂєР С›


    order = relationship(


        "Order",


        back_populates="payment",


        lazy="selectin",


    )





    bank_account_id: Mapped[int] = mapped_column(


        ForeignKey("bank_accounts.id"),


        nullable=False,


    )





    method: Mapped[PaymentMethod] = mapped_column(


        Enum(PaymentMethod),


        nullable=False,


    )





    status: Mapped[PaymentStatus] = mapped_column(


        Enum(PaymentStatus),


        nullable=False,


    )





    amount: Mapped[int] = mapped_column(Integer, nullable=False)





    requisites: Mapped[str] = mapped_column(String(255), nullable=False)





    check_file_id: Mapped[str | None] = mapped_column(String(255))


    reject_reason: Mapped[str | None] = mapped_column(String(255))





    created_at: Mapped[datetime] = mapped_column(


        DateTime, default=datetime.utcnow


    )


    approved_at: Mapped[datetime | None] = mapped_column(DateTime)


    rejected_at: Mapped[datetime | None] = mapped_column(DateTime)





    bank_account = relationship("BankAccount")





