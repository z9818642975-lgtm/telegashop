from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB


def iam_here_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Я на месте",
                    callback_data=CB.OP_ALIVE,
                )
            ]
        ]
    )

