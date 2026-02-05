# bot/services/order_price.py
from decimal import Decimal
from typing import Iterable


def calculate_order_price(items: Iterable) -> Decimal:
    total = Decimal("0")
    for item in items:
        total += Decimal(item.price) * item.qty
    return total


