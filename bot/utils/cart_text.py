# bot/utils/cart_text.py
from decimal import Decimal


def build_cart_text(items) -> str:
    if not items:
        return "🧺 <b>Корзина пуста</b>"

    lines = ["🧺 <b>Ваша корзина:</b>\n"]
    total = Decimal("0")

    for item in items:
        price = Decimal(item.price) * item.qty
        total += price
        lines.append(f"• {item.title} × {item.qty} = {price} ₽")

    lines.append(f"\n<b>Итого:</b> {total} ₽")
    return "\n".join(lines)


