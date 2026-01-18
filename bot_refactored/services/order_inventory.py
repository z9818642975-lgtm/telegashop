from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.inventory import InventoryDAO


async def reserve_order_items(
    session: AsyncSession,
    *,
    operator_id: int,
    items: list[tuple[int, int]],  # (product_id, qty)
):
    for product_id, qty in items:
        item = await InventoryDAO.get_for_update(
            session,
            operator_id=operator_id,
            product_id=product_id,
        )
        if not item:
            raise ValueError("item not found in inventory")

        InventoryDAO.reserve(item, qty)

