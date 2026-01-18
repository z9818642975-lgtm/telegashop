# bot/services/shift_guard.py
from datetime import datetime, timedelta

# bot/services/shift_guard.py
from datetime import datetime, timedelta





from sqlalchemy import select


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.operator_shift_dao import OperatorShiftDAO


from bot.models.operator_shift import OperatorShift


from bot.exceptions import ForbiddenError





SHIFT_TTL_MINUTES = 30








async def ensure_operator_on_shift(


    session: AsyncSession,


    operator_id: int,


) -> OperatorShift:


    res = await session.execute(


        select(OperatorShift).where(


            OperatorShift.operator_id == operator_id,


            OperatorShift.ended_at.is_(None),


        )


    )


    shift = res.scalar_one_or_none()





    if not shift:


        raise ForbiddenError("Смена не начата")





    if shift.started_at < datetime.utcnow() - timedelta(minutes=SHIFT_TTL_MINUTES):


        shift.ended_at = datetime.utcnow()


        await session.flush()


        raise ForbiddenError("Смена закрыта по таймауту")





    return shift





