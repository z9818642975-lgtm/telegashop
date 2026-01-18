# bot/keyboards/inline/back.py
from aiogram.types import InlineKeyboardButton
from bot.constants.callbacks import CB

def back_btn(callback: str = CB.BACK_CATALOG) -> InlineKeyboardButton:
    InlineKeyboardButton(
    text="◀️ Назад",
    callback_data=callback,
    )

