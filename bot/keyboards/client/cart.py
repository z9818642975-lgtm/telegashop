# bot/keyboards/client/cart.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import (
    CatalogOpen,
    ClientCartCheckout,
    ClientCartClear,
    ClientItemRemove,
)


def client_cart_kb(items: list) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for item in items:
        rows.append([
            InlineKeyboardButton(
                text=f"❌ {item.product.title} × {item.qty}",
                callback_data=ClientItemRemove(item_id=item.id).pack(),
            )
        ])

    if items:
        rows.append([
            InlineKeyboardButton(
                text="🧹 Очистить корзину",
                callback_data=ClientCartClear().pack(),
            )
        ])
        rows.append([
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data=ClientCartCheckout().pack(),
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="⬅️ В каталог",
            callback_data=CatalogOpen().pack(),
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)