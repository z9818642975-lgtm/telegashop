from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.inventory_log import InventoryLog

class InventoryLogDAO:
    @staticmethod
    async def write(session: AsyncSession, operator_id: int, product_id: int, qty: int):
        session.add(
            InventoryLog(
                operator_id=operator_id,
                product_id=product_id,
                qty=qty,
            )
        )

    @staticmethod
    async def report(session: AsyncSession):
        res = await session.execute(select(InventoryLog))
        return res.scalars().all()

