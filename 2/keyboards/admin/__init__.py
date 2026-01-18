# bot/keyboards/admin/__init__.py

from bot.keyboards.admin.main import admin_main_menu
from bot.keyboards.admin.panel import admin_panel_kb
#from bot.keyboards.admin.banks import banks_kb

from bot.keyboards.admin.warehouses import warehouses_kb
from bot.keyboards.admin.warehouse_actions import warehouse_actions_kb
from bot.keyboards.admin.force_actions import force_actions_kb

__all__ = [
    "admin_main_menu",
    "admin_panel_kb",
    "warehouses_kb",
    "warehouse_actions_kb",
    "force_actions_kb",
]

