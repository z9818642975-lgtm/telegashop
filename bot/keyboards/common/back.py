# bot/keyboards/common/back.py
# bot/keyboards/inline/back.py
from aiogram.types import InlineKeyboardButton

from bot.constants.callbacks_common import ClientCartOpen


def back_btn(callback: str = "") -> InlineKeyboardButton:
    InlineKeyboardButton(
    text="◀️ Назад",
    callback_data=ClientCartOpen().pack(),
    )









