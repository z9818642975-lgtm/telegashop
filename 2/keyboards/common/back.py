# bot/keyboards/inline/back.py
from aiogram.types import InlineKeyboardButton
from bot.constants.callbacks import CB

def back_btn(callback: str = CB.BACK_CATALOG) -> InlineKeyboardButton:
    return InlineKeyboardButton("в¬…пёЏ РќР°Р·Р°Рґ", callback_data=callback)

