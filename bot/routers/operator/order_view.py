# bot/routers/operator/order_view.py
from aiogram import Router

# bot/routers/operator/order_view.py
from aiogram.types import Message

router = Router(name="operator_order_view")








@router.message()


async def view_order(message: Message):


    await message.answer("Просмотр заказа")








