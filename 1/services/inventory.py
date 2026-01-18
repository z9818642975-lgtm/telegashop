from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models.order_item import OrderItem
from bot.models.product import Product

class InventoryService:
    @staticmethod
    async def deduct(session: AsyncSession, order_id: int) -> None:
        result = await session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        items = result.scalars().all()

        for item in items:
            product = await session.get(Product, item.product_id)
            if product.stock < item.qty:
                raise ValueError("РќРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ РѕСЃС‚Р°С‚РєРѕРІ")

            product.stock -= item.qty

