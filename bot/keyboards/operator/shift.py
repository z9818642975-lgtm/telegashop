from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.actions.operator import OperatorAction
from bot.constants.action_cb import ActionCB


def operator_shift_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="О ▶️ Начать смену",
                    callback_data=ActionCB(
                        action=OperatorAction.SHIFT_START
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="О ⏹ Завершить смену",
                    callback_data=ActionCB(
                        action=OperatorAction.SHIFT_STOP
                    ).pack(),
                )
            ],
        ]
    )