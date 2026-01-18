# bot/keyboards/admin/main.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="СЂСџвЂњВ¦ Р СћР С•Р Р†Р В°РЎР‚РЎвЂ№"),
                KeyboardButton(text="СЂСџРЏВ¦ Р вЂР В°Р Р…Р С”Р С‘"),
            ],
            [
                KeyboardButton(text="СЂСџвЂВ· Р С›Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎвЂ№"),
                KeyboardButton(text="СЂСџРЏВ¬ Р РЋР С”Р В»Р В°Р Т‘РЎвЂ№"),
            ],
            [
                KeyboardButton(text="СЂСџвЂњР‰ Р РЋРЎвЂљР В°РЎвЂљР С‘РЎРѓРЎвЂљР С‘Р С”Р В°"),
            ],
        ],
        resize_keyboard=True,
        selective=True,
    )

