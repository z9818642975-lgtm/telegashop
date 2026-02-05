# bot/keyboards/operator/statistics.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorSalaryStatsCB


def operator_stats_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 📆 День",
                    callback_data=OperatorSalaryStatsCB(period="day").pack(),
                ),
                InlineKeyboardButton(
                    text="О 📆 Неделя",
                    callback_data=OperatorSalaryStatsCB(period="week").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="О 📆 Месяц",
                    callback_data=OperatorSalaryStatsCB(period="month").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="О ⬅️ В корзину",
                    callback_data=OperatorSalaryStatsCB(period="back").pack(),
                ),
            ],
        ]
    )