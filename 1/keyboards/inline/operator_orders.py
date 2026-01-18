from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

def operator_orders_kb(page: int, has_prev: bool, has_next: bool):
    buttons = []
    row = []

    if has_prev:
        row.append(
            InlineKeyboardButton(
                "в¬…пёЏ",
                callback_data=f"{CB.OP_ORDERS_PAGE}{page-1}",
            )
        )
    if has_next:
        row.append(
            InlineKeyboardButton(
                "вћЎпёЏ",
                callback_data=f"{CB.OP_ORDERS_PAGE}{page+1}",
            )
        )

    if row:
        buttons.append(row)

    buttons.append(
        [InlineKeyboardButton("рџ”™ Р’РµСЂРЅСѓС‚СЊСЃСЏ", callback_data=CB.OP_PANEL)]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

