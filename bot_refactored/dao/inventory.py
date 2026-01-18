from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.inventory import InventoryItem


class InventoryDAO:

    @staticmethod
    async def get_for_update(
        session: AsyncSession,
        *,
        operator_id: int,
        product_id: int,
    ) -> InventoryItem | None:
        stmt = (
            select(InventoryItem)
            .where(
                InventoryItem.operator_id == operator_id,
                InventoryItem.product_id == product_id,
            )
            .with_for_update()
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    def reserve(item: InventoryItem, qty: int):
        if item.quantity - item.reserved < qty:
            raise ValueError("not enough stock")
        item.reserved += qty

    @staticmethod
    def commit(item: InventoryItem, qty: int):
        item.quantity -= qty
        item.reserved -= qty

    @staticmethod
    def rollback(item: InventoryItem, qty: int):
        item.reserved -= qty

