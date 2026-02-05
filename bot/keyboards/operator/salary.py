# bot/keyboards/operator/salary.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorSalaryPayoutCB, OperatorSalaryStatsCB


def operator_salary_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О 📊 День",
                    callback_data=OperatorSalaryStatsCB(period="day").pack(),
                ),
                InlineKeyboardButton(
                    text="О 📊 Неделя",
                    callback_data=OperatorSalaryStatsCB(period="week").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="О 📊 Месяц",
                    callback_data=OperatorSalaryStatsCB(period="month").pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="О 💸 Запросить выплату",
                    callback_data=OperatorSalaryPayoutCB().pack(),
                ),
            ],
        ]
    )