from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

def back_kb(target: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("рџ”™ Р’РµСЂРЅСѓС‚СЊСЃСЏ", callback_data=target)]
        ]
    )

