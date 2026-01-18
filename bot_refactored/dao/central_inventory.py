from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.central_inventory import CentralInventory

class CentralInventoryDAO:
    @staticmethod
    async def get_for_update(session: AsyncSession, product_id: int):
        res = await session.execute(
            select(CentralInventory)
            .where(CentralInventory.product_id == product_id)
            .with_for_update()
        )
        return res.scalar_one_or_none()

