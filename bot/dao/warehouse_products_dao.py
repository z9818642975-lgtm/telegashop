from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.warehouse_product import WarehouseProduct

class WarehouseProductsDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get_row(self, warehouse_id: int, product_id: int):
        res = await self.s.execute(select(WarehouseProduct).where(WarehouseProduct.warehouse_id==warehouse_id, WarehouseProduct.product_id==product_id))
        return res.scalar_one_or_none()

    async def get_qty(self, warehouse_id: int, product_id: int) -> int:
        row = await self.get_row(warehouse_id, product_id)
        return row.qty_available if row else 0

    async def decrease(self, warehouse_id: int, product_id: int, qty: int):
        await self.s.execute(
            update(WarehouseProduct)
            .where(WarehouseProduct.warehouse_id==warehouse_id, WarehouseProduct.product_id==product_id)
            .values(qty_available=WarehouseProduct.qty_available - qty)
        )
