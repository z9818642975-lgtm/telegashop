# bot/routers/operator/alive.py

# bot/routers/operator/alive.py
# bot/routers/operator/alive.py


from aiogram import Router, F


from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.operator_shift_dao import OperatorShiftDAO


from bot.models.user import User


from bot.constants.callbacks import CB





router = Router(name="operator_alive")








@router.callback_query(F.data == CB.OP_ALIVE)


async def operator_alive(cb, *, session: AsyncSession | None = None,


    user: User,


):


    await cb.answer("СЂСџСџСћ Р С›Р Р…Р В»Р В°Р в„–Р Р…")





    dao = OperatorShiftDAO(session)


    await dao.touch_alive(operator_id=user.id)






