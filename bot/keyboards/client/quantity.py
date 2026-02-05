# bot/keyboards/client/quantity.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientCartOpen, ClientItemQty


def client_quantity_kb(item_id: int) -> InlineKeyboardMarkup:
    rows = []

    rows.append([
        InlineKeyboardButton(
            text=str(q),
            callback_data=ClientItemQty(item_id=item_id, qty=q).pack(),
        )
        for q in range(1, 6)
    ])

    rows.append([
        InlineKeyboardButton(
            text=str(q),
            callback_data=ClientItemQty(item_id=item_id, qty=q).pack(),
        )
        for q in range(6, 11)
    ])

    rows.append([
        InlineKeyboardButton(
            text="⬅️ В корзину",
            callback_data=ClientCartOpen().pack(),
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)