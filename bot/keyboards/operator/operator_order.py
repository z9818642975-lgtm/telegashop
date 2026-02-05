# bot/keyboards/operator/operator_order.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorDeliverySentCB, OperatorReady


def operator_order_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О ✅ Готов",
                    callback_data=OperatorReady(order_id=order_id).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="О 🚚 Отправлен",
                    callback_data=OperatorDeliverySentCB(order_id=order_id).pack(),
                )
            ],
        ]
    )