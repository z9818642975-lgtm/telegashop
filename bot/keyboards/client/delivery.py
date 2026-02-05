# bot/keyboards/client/delivery.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientDeliveryCourier, ClientDeliveryPickup
from bot.constants.callbacks_common import BackCB


def client_delivery_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
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
                    callback_data=BackCB(target="client_menu").pack()
                )
            ],
        ]
    )