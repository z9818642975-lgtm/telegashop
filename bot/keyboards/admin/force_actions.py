# bot/keyboards/admin/force_actions.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminOrderForce


def force_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 🛑 Принудительно закрыть",
                    callback_data=AdminOrderForce(
                        order_id=order_id
                    ).pack(),
                ),
            ],
        ]
    )