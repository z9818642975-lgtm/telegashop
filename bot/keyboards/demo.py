# bot/keyboards/demo.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_demo import DemoCB


def demo_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Кнопка A",
                    callback_data=DemoCB(action="a").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔵 Кнопка B",
                    callback_data=DemoCB(action="b").pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 Кнопка C",
                    callback_data=DemoCB(action="c").pack()
                )
            ],
        ]
    )