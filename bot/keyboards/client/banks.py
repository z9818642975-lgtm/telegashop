# bot/keyboards/client/banks.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientPayBank, ClientPaySBP


def client_banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏦 Сбер",
                    callback_data=ClientPayBank(bank_id=1).pack(),
                ),
                InlineKeyboardButton(
                    text="🏦 Т-Банк",
                    callback_data=ClientPayBank(bank_id=2).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏦 Альфа",
                    callback_data=ClientPayBank(bank_id=3).pack(),
                ),
                InlineKeyboardButton(
                    text="📱 СБП",
                    callback_data=ClientPaySBP().pack(),
                ),
            ],
        ]
    )