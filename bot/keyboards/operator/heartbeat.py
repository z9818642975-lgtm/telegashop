# bot/keyboards/operator/heartbeat.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def iam_here_kb(shift_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 🟢 Я на месте",
                )
            ]
        ]
    )