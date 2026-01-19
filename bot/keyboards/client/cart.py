from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Iterable


def cart_inline_kb(items: Iterable) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    for item in items:
        item_id = item.id

        # 1–5
        keyboard.append([
            InlineKeyboardButton(
                text=str(i),
                callback_data=f"client:item:qty:{item_id}:{i}"
            )
            for i in range(1, 6)
        ])

        # 6–10
        keyboard.append([
            InlineKeyboardButton(
                text=str(i),
                callback_data=f"client:item:qty:{item_id}:{i}"
            )
            for i in range(6, 11)
        ])

        # удалить
        keyboard.append([
            InlineKeyboardButton(
                text="❌ Удалить",
                callback_data=f"client:item:remove:{item_id}"
            )
        ])

    # очистить корзину
    keyboard.append([
        InlineKeyboardButton(
            text="🗑 Очистить корзину",
            callback_data="client:cart:clear"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
