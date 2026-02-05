from __future__ import annotations

from typing import TYPE_CHECKING

# bot/models/__init__.py
from bot.models.bank_account import BankAccount
from bot.models.enums import OrderItemStatus, OrderStatus, UserRole
from bot.models.operator_shift import OperatorShift
from bot.models.order import Order
from bot.models.order_item import OrderItem
from bot.models.payment import Payment
from bot.models.product import Product
from bot.models.salary_accrual import SalaryAccrual
from bot.models.user import User
from bot.models.warehouse import Warehouse
from bot.models.warehouse_movement import WarehouseMovement
from bot.models.warehouse_product import WarehouseProduct

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .payment import Payment
    from .user import User

__all__ = [
    "User",
    "Product",
    "Warehouse",
    "WarehouseProduct",
    "WarehouseMovement",
    "OperatorShift",
    "Order",
    "OrderItem",
    "BankAccount",
    "SalaryAccrual",
    "Payment",
    "UserRole",
    "OrderStatus",
    "OrderItemStatus",
]

# noqa: F821
