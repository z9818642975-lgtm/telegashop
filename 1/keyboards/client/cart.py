from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB
from bot.models.order_item import OrderItem


def cart_inline_kb(items: list[OrderItem]) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    for item in items:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"❌ Убрать {item.product.title}",
                    callback_data=f"{CB.CART_REMOVE}:{item.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🗑 Очистить корзину",
                callback_data=CB.CART_CLEAR,
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ В каталог",
                callback_data=CB.BACK_CATALOG,
            ),
            InlineKeyboardButton(
                text="✅ Оформить заказ",
                callback_data=CB.CART_CHECKOUT,
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

