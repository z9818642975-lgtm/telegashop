from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def operator_shift_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="рџ“Ќ РЈРєР°Р·Р°С‚СЊ Р°РґСЂРµСЃ СЃР°РјРѕРІС‹РІРѕР·Р°")],
            [KeyboardButton(text="в¬… РќР°Р·Р°Рґ")],
        ],
        resize_keyboard=True,
    )

