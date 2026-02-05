# bot/middlewares/shift_guard.py
# bot/services/shift_guard.py

# bot/middlewares/shift_guard.py
# bot/services/shift_guard.py





from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.exceptions import ForbiddenError
from bot.models.operator_shift import OperatorShift

SHIFT_TTL_MINUTES = 30








async def ensure_operator_on_shift(


    *,


    session: AsyncSession,


    operator_id: int,


) -> OperatorShift:


    """


    Проверяет, что оператор находится на активной смене.





    ✔ если смены нет → ForbiddenError


    ✔ если смена протухла → автозакрытие + ForbiddenError


    ✔ если всё ок → возвращает OperatorShift


    """





    result = await session.execute(


        select(OperatorShift).where(


            OperatorShift.operator_id == operator_id,


            OperatorShift.ended_at.is_(None),


        )


    )


    shift = result.scalar_one_or_none()





    if not shift:


        raise ForbiddenError("❌ Смена не начата")





    now = datetime.utcnow()





    if shift.started_at < now - timedelta(minutes=SHIFT_TTL_MINUTES):


        shift.ended_at = now


        await session.flush()


        raise ForbiddenError("⏱ Смена закрыта по таймауту")





    return shift






