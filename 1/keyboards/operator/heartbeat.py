from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB


def iam_here_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџСџСћ Р Р‡ Р Р…Р В° Р СР ВµРЎРѓРЎвЂљР Вµ",
                    callback_data=CB.OP_ALIVE,
                )
            ]
        ]
    )

