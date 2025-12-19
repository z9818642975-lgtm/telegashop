from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.restock_order import RestockOrder

class RestockDAO:
    def __init__(self, s: AsyncSession): self.s = s
    async def has_active(self, product_id: int, warehouse_id: int):
        res = await self.s.execute(select(RestockOrder).where(RestockOrder.product_id==product_id, RestockOrder.warehouse_id==warehouse_id, RestockOrder.status.in_(["CREATED","SENT"])))
        return res.scalar_one_or_none() is not None
    async def create(self, **data):
        r = RestockOrder(**data)
        self.s.add(r); await self.s.flush()
        return r
