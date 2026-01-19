# bot/routers/client/delivery_price.py
from aiogram import Router, F

# bot/routers/client/delivery_price.py
from aiogram import Router, F


from aiogram.types import CallbackQuery





router = Router(name="client_delivery_price")





@router.callback_query(F.data.startswith("client:delivery_price:"))


async def price(cb: CallbackQuery):


    await cb.answer("Цена доставки выбрана")





