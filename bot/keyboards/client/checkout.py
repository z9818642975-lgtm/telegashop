from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import (
    ClientCartOpen,
    ClientDeliveryCourier,
    ClientDeliveryPickup,
)


def client_checkout_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📍 Самовывоз",
                callback_data=ClientDeliveryPickup().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🚚 Курьер",
                callback_data=ClientDeliveryCourier().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ В корзину",
                callback_data=ClientCartOpen().pack(),
            )
        ],
    ])
