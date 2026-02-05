# bot/keyboards/admin/products.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminProductCard


def admin_products_kb(products: list) -> InlineKeyboardMarkup:
    rows = []
    for p in products:
        rows.append(
            [
                InlineKeyboardButton(
                    text=p.title,
                    callback_data=AdminProductCard(product_id=p.id).pack(),
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)