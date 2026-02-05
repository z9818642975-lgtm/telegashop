# bot/keyboards/operator/pickup_confirm.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorReady


def pickup_confirm_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 📦 Самовывоз подтверждён",
                    callback_data=OperatorReady(order_id=order_id).pack(),
                )
            ]
        ]
    )