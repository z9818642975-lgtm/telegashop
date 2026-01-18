from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def checkout_kb() -> InlineKeyboardMarkup:
    """
    Первый экран чекаута (из корзины)
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚚 Выбрать способ доставки",
                    callback_data=CB.CART_CHECKOUT,
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ В корзину",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )


def delivery_type_kb() -> InlineKeyboardMarkup:
    """
    Выбор типа доставки
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Самовывоз",
                    callback_data=CB.DELIVERY_PICKUP,
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚚 Курьер",
                    callback_data=CB.DELIVERY_COURIER,
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ В корзину",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )

