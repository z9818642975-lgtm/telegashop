from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

def admin_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("рџ“Љ SLA РѕРїРµСЂР°С‚РѕСЂРѕРІ", callback_data=CB.ADMIN_SLA)],
            [InlineKeyboardButton("рџ’° Р—Р°СЂРїР»Р°С‚Р° РѕРїРµСЂР°С‚РѕСЂРѕРІ", callback_data=CB.ADMIN_SALARY)],
        ]
    )

