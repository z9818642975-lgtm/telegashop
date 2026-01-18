from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.product import Product


class ProductsDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active(self) -> list[Product]:
        res = await self.session.execute(
            select(Product).where(Product.is_active.is_(True))
        )
        return list(res.scalars())

    async def get_by_id(self, product_id: int) -> Product | None:
        res = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return res.scalar_one_or_none()

