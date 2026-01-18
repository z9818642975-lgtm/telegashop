# bot/routers/operator/callbacks.py
from aiogram import Router

# bot/routers/operator/callbacks.py
from aiogram import Router


from aiogram.types import CallbackQuery





router = Router(name="operator_callbacks")








@router.callback_query()


async def operator_callback(cb: CallbackQuery):


    await cb.answer("OK")





