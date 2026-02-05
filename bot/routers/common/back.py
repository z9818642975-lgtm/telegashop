# bot/routers/common/back.py
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.constants.callbacks_common import ClientBackCatalog, ClientBackMenu
from bot.keyboards.reply.client_menu import client_main_menu_kb

router = Router()


@router.callback_query(ClientBackMenu.filter())
async def back_menu(cb: CallbackQuery):
    await cb.message.answer(
        "Главное меню",
        reply_markup=client_main_menu_kb(),
    )
    await cb.answer()


@router.callback_query(ClientBackCatalog.filter())
async def back_catalog(cb: CallbackQuery):
    await cb.message.answer(
        "📦 Откройте каталог через меню",
        reply_markup=client_main_menu_kb(),
    )
    await cb.answer()