# bot/keyboards/admin/__init__.py
from .banks import admin_banks_kb
from .force_actions import force_actions_kb
from .main import admin_main_menu_kb
from .operators import admin_operators_kb
from .products import admin_products_kb
from .warehouse_actions import warehouse_actions_kb
from .warehouses import warehouses_kb

__all__ = [
    "admin_banks_kb",
    "force_actions_kb",
    "admin_operators_kb",
    "admin_main_menu_kb",
    "admin_products_kb",
    "warehouse_actions_kb",
    "warehouses_kb",
]