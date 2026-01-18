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


async def operator_alive(


    cb: CallbackQuery,


    session: AsyncSession,


    user: User,


):


    await cb.answer("🟢 Онлайн")





    dao = OperatorShiftDAO(session)


    await dao.touch_alive(operator_id=user.id)




