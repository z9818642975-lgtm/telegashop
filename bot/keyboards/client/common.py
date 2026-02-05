# bot/keyboards/client/common.py
from aiogram.types import InlineKeyboardButton

from bot.constants.callbacks_client import ClientCartOpen


def back_btn(text: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=ClientCartOpen().pack(),
    )


