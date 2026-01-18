# bot/keyboards/client/banks.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏦 Сбер",
                    callback_data="bank:sber",
                ),
                InlineKeyboardButton(
                    text="🏦 Т-Банк",
                    callback_data="bank:tinkoff",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏦 Альфа",
                    callback_data="bank:alfa",
                ),
                InlineKeyboardButton(
                    text="⚡ СБП",
                    callback_data="bank:sbp",
                ),
            ],
        ]
    )

