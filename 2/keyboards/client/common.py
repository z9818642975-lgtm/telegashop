# bot/keyboards/client/common.py

from aiogram.types import InlineKeyboardButton


def back_btn(text: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=callback_data,
    )

