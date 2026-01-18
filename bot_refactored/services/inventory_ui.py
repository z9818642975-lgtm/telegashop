from bot_refactored.models.inventory import InventoryItem

def render_operator_inventory(items: list[InventoryItem]) -> str:
    lines = ["📦 Ваши остатки:"]
    for i in items:
        free = i.quantity - i.reserved
        lines.append(
            f"Товар {i.product_id}: свободно {free}, резерв {i.reserved}"
        )
    return "\n".join(lines)

def render_admin_inventory(items: list[InventoryItem]) -> str:
    lines = ["📦 Остатки по операторам:"]
    for i in items:
        lines.append(
            f"Оператор {i.operator_id}, товар {i.product_id}: "
            f"{i.quantity} (резерв {i.reserved})"
        )
    return "\n".join(lines)

