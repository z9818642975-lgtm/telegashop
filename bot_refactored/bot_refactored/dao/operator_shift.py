from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.operator_shift import OperatorShift, ShiftState


class OperatorShiftDAO:

    @staticmethod
    async def get_active_for_update(session: AsyncSession, operator_id: int):
        stmt = (
            select(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.state == ShiftState.OPEN,
            )
            .with_for_update()
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def create_open(session: AsyncSession, operator_id: int, address: str):
        shift = OperatorShift(
            operator_id=operator_id,
            state=ShiftState.OPEN,
            opened_at=datetime.utcnow(),
            pickup_address=address,
        )
        session.add(shift)
        return shift

    @staticmethod
    async def close(shift: OperatorShift):
        shift.state = ShiftState.CLOSED
        shift.closed_at = datetime.utcnow()

