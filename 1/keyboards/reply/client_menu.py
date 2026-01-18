from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def client_main_menu() -> ReplyKeyboardMarkup:
    """
    Р—Р°РіР»СѓС€РєР° РєР»РёРµРЅС‚СЃРєРѕРіРѕ РіР»Р°РІРЅРѕРіРѕ РјРµРЅСЋ.
    Р‘СѓРґРµС‚ СЂР°СЃС€РёСЂРµРЅР° РїРѕР·Р¶Рµ.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="рџ“¦ РљР°С‚Р°Р»РѕРі")],
            [KeyboardButton(text="рџ›’ РљРѕСЂР·РёРЅР°")],
        ],
        resize_keyboard=True,
    )

