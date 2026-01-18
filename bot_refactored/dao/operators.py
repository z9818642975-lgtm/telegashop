from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.operator import Operator

class OperatorsDAO:
    @staticmethod
    async def create(session: AsyncSession, telegram_id: int):
        op = Operator(telegram_id=telegram_id, is_active=True)
        session.add(op)
        return op

    @staticmethod
    async def archive(session: AsyncSession, telegram_id: int):
        res = await session.execute(
            select(Operator).where(Operator.telegram_id == telegram_id)
        )
        op = res.scalar_one_or_none()
        if not op:
            raise ValueError("operator not found")
        op.is_active = False
        return op

    @staticmethod
    async def list_all(session: AsyncSession):
        res = await session.execute(select(Operator))
        return res.scalars().all()

