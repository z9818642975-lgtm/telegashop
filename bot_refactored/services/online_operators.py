from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.operator_shift import OperatorShift, ShiftState


async def get_online_operators(session: AsyncSession):
    stmt = select(OperatorShift).where(OperatorShift.state == ShiftState.OPEN)
    res = await session.execute(stmt)
    return res.scalars().all()

