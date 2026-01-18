from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models.product import Product
from bot.constants.callbacks import CB


def catalog_kb(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product.title} — {product.base_price} ₽",
                callback_data=f"{CB.PRODUCT_OPEN}:{product.id}",
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🧺 Корзина",
                callback_data=CB.CART_OPEN,
            ),
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data=CB.CART_CHECKOUT,
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
