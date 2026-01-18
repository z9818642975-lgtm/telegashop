from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

def operator_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("рџ“‹ Р—Р°РєР°Р·С‹ РЅР° РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ", callback_data=CB.OPERATOR_ORDERS)],
        ]
    )

