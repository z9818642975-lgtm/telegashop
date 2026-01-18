# bot/services/statistics_service.py
from sqlalchemy import select, func

# bot/services/statistics_service.py
from sqlalchemy import select, func


from bot.models.order import Order


from bot.models.salary_accrual import SalaryAccrual


from bot.models.operator_shift import OperatorShift





class StatisticsService:


    def __init__(self, session):


        self.session = session





    async def operator_shift_stats(self, operator_id: int):


        shift = await self.session.scalar(


            select(OperatorShift)


            .where(


                OperatorShift.operator_id == operator_id,


                OperatorShift.is_active.is_(True),


            )


        )





        if not shift:


            return None





        orders = await self.session.scalars(


            select(Order).where(Order.shift_id == shift.id)


        )


        orders = orders.all()





        paid = [o for o in orders if o.status == "PAID"]





        salary = await self.session.scalar(


            select(func.coalesce(func.sum(SalaryAccrual.amount), 0))


            .where(SalaryAccrual.operator_id == operator_id)


        )





        return {


            "orders_total": len(orders),


            "orders_paid": len(paid),


            "revenue": sum(o.total_price for o in paid),


            "salary": salary,


        }





