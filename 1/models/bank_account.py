# bot/models/bank_account.py
from __future__ import annotations

# bot/models/bank_account.py
from __future__ import annotations





from datetime import datetime





from sqlalchemy import Integer, String, Boolean, DateTime


from sqlalchemy.orm import Mapped, mapped_column





from bot.db.base import Base








class BankAccount(Base):


    __tablename__ = "bank_accounts"





    id: Mapped[int] = mapped_column(Integer, primary_key=True)





    bank_name: Mapped[str] = mapped_column(String(64), nullable=False)





    # BANK


    card_number: Mapped[str | None] = mapped_column(String(32))


    card_masked: Mapped[str | None] = mapped_column(String(32))





    # SBP


    sbp_phone: Mapped[str | None] = mapped_column(String(32))





    # STATE


    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


    disabled_until: Mapped[datetime | None] = mapped_column(DateTime)





    # LOAD BALANCING


    load: Mapped[int] = mapped_column(Integer, default=0)


    weight: Mapped[int] = mapped_column(Integer, default=100)





    def display(self) -> str:


        if self.card_masked:


            return f"{self.bank_name} РІР‚Сћ {self.card_masked}"


        if self.sbp_phone:


            return f"{self.bank_name} РІР‚Сћ {self.sbp_phone}"


        return self.bank_name





