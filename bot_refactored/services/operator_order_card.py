from bot_refactored.models.order import Order


def render_operator_order_card(order: Order) -> str:
    lines = [
        f"Заказ #{order.id}",
        f"Статус: {order.status}",
    ]

    if order.payment_photo_id:
        lines.append("Чек: приложен")
    else:
        lines.append("Чек: отсутствует")

    if order.payment_comment:
        lines.append(f"Комментарий: {order.payment_comment}")

    return "\n".join(lines)

