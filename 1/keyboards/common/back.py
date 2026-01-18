# bot/keyboards/inline/back.py
from aiogram.types import InlineKeyboardButton
from bot.constants.callbacks import CB

def back_btn(callback: str = CB.BACK_CATALOG) -> InlineKeyboardButton:
    return InlineKeyboardButton("Р Р†Р’В¬РІР‚В¦Р С—РЎвЂР РЏ Р В РЎСљР В Р’В°Р В Р’В·Р В Р’В°Р В РўвЂ", callback_data=callback)

