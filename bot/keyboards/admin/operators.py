# bot/keyboards/admin/operators.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminOperatorToggle


def admin_operators_kb(operators: list) -> InlineKeyboardMarkup:
    rows = []
    for op in operators:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"👤 {op.tg_id}",
                    callback_data=AdminOperatorToggle(operator_id=op.id).pack(),
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)