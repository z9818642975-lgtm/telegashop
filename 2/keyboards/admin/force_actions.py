# bot/keyboards/admin/force_actions.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def force_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⛔ Принудительно закрыть",
                    callback_data=f"admin:force:close:{order_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Вернуть в работу",
                    callback_data=f"admin:force:reopen:{order_id}",
                ),
            ],
        ]
    )

