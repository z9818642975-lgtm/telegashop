# bot/routers/operator/menu.py
from aiogram import Router

# bot/routers/operator/menu.py
from aiogram import Router


from aiogram.types import Message





router = Router(name="operator_menu")








@router.message()


async def operator_menu(message: Message):


    await message.answer("Операторское меню")





