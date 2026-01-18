from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.operator_shift import OperatorShift, ShiftState


WARN_1 = timedelta(minutes=15)
WARN_2 = timedelta(minutes=17)
WARN_3 = timedelta(minutes=18)
AUTO_CLOSE = timedelta(minutes=20)


async def get_inactive_shifts(session: AsyncSession):
    now = datetime.utcnow()

    stmt = select(OperatorShift).where(
        OperatorShift.state == ShiftState.OPEN
    )
    res = await session.execute(stmt)
    shifts = res.scalars().all()

    result = []
    for shift in shifts:
        delta = now - shift.opened_at
        result.append((shift, delta))

    return result

