from bot_refactored.models.inventory import InventoryItem
from bot_refactored.models.inventory_limits import InventoryLimit

def check_min_limit(item: InventoryItem, limit: InventoryLimit | None) -> bool:
    if not limit:
        return False
    return (item.quantity - item.reserved) <= limit.min_qty

