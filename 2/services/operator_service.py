# bot/services/operator_service.py
#C:\Users\1\project\bot\services\operator_service.py

# bot/services/operator_service.py
#C:\Users\1\project\bot\services\operator_service.py


from __future__ import annotations





from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.shifts_dao import OperatorShiftDAO


from bot.dao.users_dao import UsersDAO








class OperatorService:


    """


    Публичные методы принимают tg_id (Telegram user id),


    но в operator_shifts пишем users.id (int).


    """





    def __init__(self, session: AsyncSession):


        self.session = session


        self.users = UsersDAO(session)


        self.shifts = OperatorShiftDAO(session)





    async def _get_user_id_by_tg(self, tg_id: int) -> int:


        user = await self.users.get_by_tg_id(tg_id)


        if not user:


            # если у тебя есть create/get_or_create — подставь его


            raise ValueError(f"User with tg_id={tg_id} not found in DB")


        return user.id





    async def start_shift(self, operator_tg_id: int, pickup_address: str) -> bool:


        operator_id = await self._get_user_id_by_tg(operator_tg_id)


        active = await self.shifts.get_active(operator_id)


        if active:


            return False


        await self.shifts.start(operator_id, pickup_address)


        return True





    async def end_shift(self, operator_tg_id: int) -> bool:


        operator_id = await self._get_user_id_by_tg(operator_tg_id)


        ended = await self.shifts.end(operator_id)


        return ended is not None





    async def get_active_shift(self, operator_tg_id: int, user):


        operator_id = await self._get_user_id_by_tg(operator_tg_id)


        return await self.shifts.get_active(operator_id)








