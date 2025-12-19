from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.product import Product

class ProductsDAO:
    def __init__(self, s: AsyncSession): self.s = s
    async def list_active(self):
        res = await self.s.execute(select(Product).where(Product.is_active.is_(True)).order_by(Product.id.asc()))
        return res.scalars().all()
    async def get(self, product_id: int):
        res = await self.s.execute(select(Product).where(Product.id==product_id))
        return res.scalar_one()
