# bot/dao/operators_dao.py
from sqlalchemy import select, update

# bot/dao/operators_dao.py
from sqlalchemy import select, update


from sqlalchemy.ext.asyncio import AsyncSession


from bot.models.operator import Operator








class OperatorsDAO:


    def __init__(self, s: AsyncSession):


        self.s = s





    async def get_by_tg(self, tg_id: int) -> Operator | None:


        res = await self.s.execute(select(Operator).where(Operator.tg_id == tg_id))


        return res.scalar_one_or_none()





    async def list_active(self) -> list[Operator]:


        res = await self.s.execute(select(Operator).where(Operator.is_active.is_(True)).order_by(Operator.id.asc()))


        return list(res.scalars().all())





    async def upsert(self, tg_id: int, name: str) -> Operator:


        op = await self.get_by_tg(tg_id)


        if op:


            op.name = name


            op.is_active = True


            return op


        op = Operator(tg_id=tg_id, name=name, is_active=True)


        self.s.add(op)


        return op





    async def set_active(self, tg_id: int, active: bool) -> None:


        await self.s.execute(update(Operator).where(Operator.tg_id == tg_id).values(is_active=active))





