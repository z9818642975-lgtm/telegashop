# bot/middlewares/122.py
from aiogram import BaseMiddleware

# bot/middlewares/122.py
from aiogram import BaseMiddleware


from aiogram.types import TelegramObject





from bot.services.shift_guard import ensure_operator_on_shift








class ShiftGuardMiddleware(BaseMiddleware):


    async def __call__(self, handler, event: TelegramObject, data: dict):


        session = data["session"]


        user = data["user"]





        await ensure_operator_on_shift(


            session=session,


            operator_id=user.id,


        )





        return await handler(event, data)





