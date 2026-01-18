# bot/keyboards/client/__init__.py

from bot.keyboards.client.main import client_main_menu

from bot.keyboards.client.catalog import catalog_kb
from bot.keyboards.client.quantity import quantity_kb

from bot.keyboards.client.cart import cart_inline_kb
from bot.keyboards.client.checkout import checkout_kb

from bot.keyboards.client.delivery import delivery_kb
from bot.keyboards.client.payment import payment_kb, payment_confirm_kb
from bot.keyboards.client.pickup_actions import pickup_actions_kb
from bot.keyboards.client.profile import profile_kb
from bot.keyboards.client.banks import banks_kb

__all__ = [
    "client_main_menu",
    "catalog_kb",
    "quantity_kb",
    "cart_inline_kb",
    "checkout_kb",
    "delivery_kb",
    "payment_kb",
    "payment_confirm_kb",
    "banks_kb",
    "pickup_actions_kb",
    "profile_kb",
]

