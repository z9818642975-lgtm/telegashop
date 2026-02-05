# bot/keyboards/operator/operator_check.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorCheckCB


def operator_check_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 💰 Оплата прошла",
                    callback_data=OperatorCheckCB(
                        order_id=order_id,
                        result="paid",
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text="О ❌ Оплата не прошла",
                    callback_data=OperatorCheckCB(
                        order_id=order_id,
                        result="failed",
                    ).pack(),
                ),
            ]
        ]
    )