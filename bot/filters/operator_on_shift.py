# bot/filters/operator_on_shift.py
from aiogram.filters import BaseFilter

# bot/filters/operator_on_shift.py
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.models.enums import UserRole


class OperatorOnShiftFilter(BaseFilter):


    async def __call__(self, event: TelegramObject, data: dict) -> bool:


        role: UserRole = data.get("role")


        user = data.get("user")


        session: AsyncSession = data.get("session")





        if role != UserRole.OPERATOR:


            return False





        return await OperatorShiftDAO(session).is_on_shift(user.id)






