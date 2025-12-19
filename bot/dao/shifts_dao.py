from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.operator_shift import OperatorShift

class ShiftsDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get_active(self, operator_id: int):
        res = await self.s.execute(select(OperatorShift).where(OperatorShift.operator_id==operator_id, OperatorShift.ended_at.is_(None)))
        return res.scalar_one_or_none()

    async def list_active(self):
        res = await self.s.execute(select(OperatorShift).where(OperatorShift.ended_at.is_(None)))
        return res.scalars().all()

    async def close_active(self, operator_id: int, auto_closed: bool = False):
        await self.s.execute(
            update(OperatorShift)
            .where(OperatorShift.operator_id==operator_id, OperatorShift.ended_at.is_(None))
            .values(ended_at=datetime.utcnow(), auto_closed=auto_closed)
        )

    async def create(self, operator_id: int, address: str):
        rec = OperatorShift(operator_id=operator_id, pickup_address=address)
        self.s.add(rec); await self.s.flush()
        return rec
