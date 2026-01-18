from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def delivery_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Самовывоз",
                    callback_data=CB.DELIVERY_PICKUP,
                ),
                InlineKeyboardButton(
                    text="🚚 Курьер",
                    callback_data=CB.DELIVERY_COURIER,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ В корзину",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )

