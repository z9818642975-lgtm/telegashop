# bot/keyboards/client/__init__.py
from .banks import client_banks_kb
from .cart import client_cart_kb
from .catalog import client_catalog_kb
from .checkout import client_checkout_kb
from .delivery import client_delivery_kb
from .main import client_main_menu_kb
from .payment import client_payment_kb
from .pickup import client_pickup_addresses_kb
from .pickup_actions import client_pickup_actions_kb
from .profile import client_profile_kb
from .quantity import client_quantity_kb

__all__ = [
    "client_main_menu_kb",

    "client_banks_kb",
    "client_cart_kb",
    "client_catalog_kb",
    "client_checkout_kb",
    "client_delivery_kb",

    "client_payment_kb",

    "client_pickup_actions_kb",
    "client_pickup_addresses_kb",
    "client_profile_kb",
    "client_quantity_kb",
]