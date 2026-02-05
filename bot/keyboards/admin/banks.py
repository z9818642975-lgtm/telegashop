# bot/keyboards/admin/banks.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminBankToggle


def admin_banks_kb(banks: list) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for bank in banks:
        rows.append([
            InlineKeyboardButton(
                text=bank.title,
                callback_data=AdminBankToggle(bank_id=bank.id).pack(),
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)