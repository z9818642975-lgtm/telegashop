from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.operator import Operator

class OperatorsDAO:
    @staticmethod
    async def list(session: AsyncSession):
        result = await session.execute(select(Operator))
        return result.scalars().all()

    @staticmethod
    async def add(session: AsyncSession, tg_id: int):
        op = Operator(tg_id=tg_id)
        session.add(op)

    @staticmethod
    async def archive(session: AsyncSession, operator_id: int):
        op = await session.get(Operator, operator_id)
        if op:
            op.is_active = False

