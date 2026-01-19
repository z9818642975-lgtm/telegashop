# bot/keyboards/client/banks.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏦 Сбер",
                    callback_data="client:bank:sber",
                ),
                InlineKeyboardButton(
                    text="🏦 Т-Банк",
                    callback_data="client:bank:tinkoff",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏦 Альфа",
                    callback_data="client:bank:alfa",
                ),
                InlineKeyboardButton(
                    text="⚡ СБП",
                    callback_data="client:bank:sbp",
                ),
            ],
        ]
    )

