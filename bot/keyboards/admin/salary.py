# bot/keyboards/admin/salary.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminSalaryPayCB


def admin_salary_kb(accruals: list) -> InlineKeyboardMarkup:
    rows = []

    for acc in accruals:
        rows.append([
            InlineKeyboardButton(
                text=f"💸 {acc.operator_id} — {acc.amount} ₽",
                callback_data=AdminSalaryPayCB(
                    accrual_id=acc.id
                ).pack(),
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)