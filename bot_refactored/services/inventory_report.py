from bot_refactored.models.inventory_log import InventoryLog

def render_inventory_report(logs: list[InventoryLog]) -> str:
    lines = ["📊 Отчёт по списаниям:"]
    for l in logs:
        lines.append(
            f"{l.created_at} | Оператор {l.operator_id} | "
            f"Товар {l.product_id} | -{l.qty}"
        )
    return "\n".join(lines)

