from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def operator_inline_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="рџ“¦ Р—Р°РєР°Р·С‹", callback_data="operator:orders")],
        [InlineKeyboardButton(text="вЏ± РЎРјРµРЅР°", callback_data="operator:shift")],
    ])

