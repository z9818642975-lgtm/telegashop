# bot/keyboards/client/profile.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientCartOpen
from bot.constants.callbacks_common import BackCB


def client_profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📦 Мои заказы",
                callback_data=ClientCartOpen().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ В корзину",
                callback_data=BackCB(target="client_menu").pack()
            ),
        ],
    ])