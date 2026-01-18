from bot_refactored.models.order import Order


def render_orders(orders: list[Order]) -> str:
    if not orders:
        return "❌ Заказы не найдены"

    lines = ["📦 Заказы:"]
    for o in orders:
        lines.append(
            f"#{o.id} | {o.status} | "
            f"оператор: {o.operator_id or '-'} | "
            f"{o.created_at:%Y-%m-%d %H:%M}"
        )
    return "\n".join(lines)

