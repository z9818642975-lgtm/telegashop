from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def client_inline_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="рџ“¦ РљР°С‚Р°Р»РѕРі", callback_data="client:catalog")],
        [InlineKeyboardButton(text="рџ›’ РљРѕСЂР·РёРЅР°", callback_data="client:cart")],
    ])

