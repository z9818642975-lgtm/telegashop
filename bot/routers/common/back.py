# bot/routers/common/back.py
from aiogram import Router, F

# bot/routers/common/back.py
from aiogram import Router, F


from aiogram.types import CallbackQuery





from bot.constants.callbacks import CB


from bot.keyboards.reply.client_menu import client_main_menu





router = Router()








@router.callback_query(F.data == CB.BACK_MENU)


async def back_menu(call: CallbackQuery):


    await call.message.answer(


        "Главное меню",


        reply_markup=client_main_menu(),


    )








@router.callback_query(F.data == CB.BACK_CATALOG)


async def back_catalog(call: CallbackQuery):


    await call.message.answer(


        "📦 Откройте каталог через меню",


        reply_markup=client_main_menu(),


    )





