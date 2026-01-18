# bot/dao/salary_dao.py
from sqlalchemy import select, update

# bot/dao/salary_dao.py
from sqlalchemy import select, update


from sqlalchemy.ext.asyncio import AsyncSession





from bot.models.salary_accrual import SalaryAccrual








class SalaryDAO:


    def __init__(self, session: AsyncSession):


        self.session = session





    async def create(


        self,


        *,


        operator_id: int,


        amount: int,


        order_id: int | None = None,


    ) -> SalaryAccrual:


        row = SalaryAccrual(


            operator_id=operator_id,


            order_id=order_id,


            amount=amount,


            status="NEW",


        )


        self.session.add(row)


        await self.session.flush()


        return row





    async def list_by_operator(self, operator_id: int):


        res = await self.session.execute(


            select(SalaryAccrual)


            .where(SalaryAccrual.operator_id == operator_id)


            .order_by(SalaryAccrual.created_at.desc())


        )


        return res.scalars().all()





    async def request_payout(self, operator_id: int):


        await self.session.execute(


            update(SalaryAccrual)


            .where(


                SalaryAccrual.operator_id == operator_id,


                SalaryAccrual.status == "NEW",


            )


            .values(status="REQUESTED")


        )





    async def list_requested(self):


        res = await self.session.execute(


            select(SalaryAccrual)


            .where(SalaryAccrual.status == "REQUESTED")


        )


        return res.scalars().all()





    async def mark_paid(self, ids: list[int]):


        if not ids:


            return





        await self.session.execute(


            update(SalaryAccrual)


            .where(SalaryAccrual.id.in_(ids))


            .values(status="PAID")


        )





