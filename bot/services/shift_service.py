# bot/services/shift_service.py
from sqlalchemy import select

# bot/services/shift_service.py
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.operator_shift import OperatorShift


class ShiftService:


    def __init__(self, session: AsyncSession):


        self.s = session





    async def is_on_shift(self, operator_tg_id: int) -> bool:


        res = await self.s.execute(


            select(OperatorShift).where(


                OperatorShift.operator_id == operator_tg_id,


                OperatorShift.ended_at.is_(None)


            )


        )


        return res.scalar_one_or_none() is not None







