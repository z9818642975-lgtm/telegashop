# bot/keyboards/operator/orders.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorOrdersCB


def operator_orders_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 📦 Активные заказы",
                    callback_data=OperatorOrdersCB(action="active").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="О ✅ Завершённые",
                    callback_data=OperatorOrdersCB(action="done").pack(),
                )
            ],
        ]
    )