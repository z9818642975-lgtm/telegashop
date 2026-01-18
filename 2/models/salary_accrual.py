# bot/models/salary_accrual.py
from datetime import datetime

# bot/models/salary_accrual.py
from datetime import datetime





from sqlalchemy import ForeignKey, Integer, DateTime


from sqlalchemy.orm import Mapped, mapped_column





from bot.db.base import Base








class SalaryAccrual(Base):


    __tablename__ = "salary_accruals"





    id: Mapped[int] = mapped_column(primary_key=True)





    operator_id: Mapped[int] = mapped_column(


        ForeignKey("users.id", ondelete="CASCADE"),


        nullable=False,


    )





    order_item_id: Mapped[int] = mapped_column(


        ForeignKey("order_items.id", ondelete="CASCADE"),


        nullable=False,


    )





    amount: Mapped[int] = mapped_column(Integer, nullable=False)





    created_at: Mapped[datetime] = mapped_column(


        DateTime,


        default=datetime.utcnow,


        nullable=False,


    )





