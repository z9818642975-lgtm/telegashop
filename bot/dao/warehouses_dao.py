from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.warehouse import Warehouse

class WarehousesDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get_admin(self):
        res = await self.s.execute(select(Warehouse).where(Warehouse.type=="ADMIN", Warehouse.is_active.is_(True)))
        return res.scalar_one()

    async def get_operator(self, operator_tg_id: int):
        res = await self.s.execute(select(Warehouse).where(Warehouse.type=="OPERATOR", Warehouse.owner_id==operator_tg_id, Warehouse.is_active.is_(True)))
        return res.scalar_one_or_none()
