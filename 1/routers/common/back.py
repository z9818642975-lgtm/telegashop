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


        "Р вЂњР В»Р В°Р Р†Р Р…Р С•Р Вµ Р СР ВµР Р…РЎР‹",


        reply_markup=client_main_menu(),


    )








@router.callback_query(F.data == CB.BACK_CATALOG)


async def back_catalog(call: CallbackQuery):


    await call.message.answer(


        "СЂСџвЂњВ¦ Р С›РЎвЂљР С”РЎР‚Р С•Р в„–РЎвЂљР Вµ Р С”Р В°РЎвЂљР В°Р В»Р С•Р С– РЎвЂЎР ВµРЎР‚Р ВµР В· Р СР ВµР Р…РЎР‹",


        reply_markup=client_main_menu(),


    )





