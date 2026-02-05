# bot/dao/pickup_dao.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.operator_shift import OperatorShift


class PickupDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_online(self):
        stmt = select(OperatorShift).where(
            OperatorShift.ended_at.is_(None),
            OperatorShift.pickup_address.is_not(None),
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()


