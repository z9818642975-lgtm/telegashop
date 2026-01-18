from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.product import Product


class ProductsDAO:
    @staticmethod
    async def get_active(session: AsyncSession):
        res = await session.execute(
            select(Product).where(Product.is_active.is_(True))
        )
        return res.scalars().all()

    @staticmethod
    async def get_by_id(session: AsyncSession, product_id: int):
        res = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return res.scalar_one_or_none()

