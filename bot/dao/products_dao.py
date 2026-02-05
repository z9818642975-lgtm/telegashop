# bot/dao/products_dao.py
from sqlalchemy import select

from bot.dao.base import BaseDAO
from bot.models.product import Product


class ProductsDAO(BaseDAO):

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
