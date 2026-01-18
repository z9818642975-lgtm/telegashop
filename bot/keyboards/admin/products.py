from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.product import Product


def products_kb(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard = []

    for p in products:
        status = "🟢" if p.is_active else "⚫️"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{status} {p.title} ({p.base_price} ₽)",
                    callback_data=f"admin:product:card:{p.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить товар",
                callback_data="admin:product:create",
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin:panel",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

