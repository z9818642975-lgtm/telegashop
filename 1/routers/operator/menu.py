from aiogram import Router, F
from aiogram.types import Message

from bot.models.user import User
from bot.keyboards.operator.menu import operator_main_menu

router = Router(name="operator_menu")


# ❌ DISABLED (text-based handler)
async def operator_menu(
    message: Message,
    *,
    user: User | None = None,
):
    """
    Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ РѕРїРµСЂР°С‚РѕСЂР°.
    """
    await message.answer(
        "рџ‘ЁвЂЌрџ’ј <b>РњРµРЅСЋ РѕРїРµСЂР°С‚РѕСЂР°</b>",
        reply_markup=operator_main_menu(),
    )

