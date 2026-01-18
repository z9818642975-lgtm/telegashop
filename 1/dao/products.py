from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.product import Product

class ProductsDAO:
    @staticmethod
    async def list(session: AsyncSession):
        result = await session.execute(select(Product))
        return result.scalars().all()

