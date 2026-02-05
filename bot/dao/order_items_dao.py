# bot/dao/order_items_dao.py
from sqlalchemy import select

from bot.dao.base import BaseDAO
from bot.models import OrderItem


class OrderItemsDAO(BaseDAO):

    async def add_or_increment(
        self,
        order_id: int,
        product_id: int,
        qty: int,
    ) -> OrderItem:
        res = await self.session.execute(
            select(OrderItem).where(
                OrderItem.order_id == order_id,
                OrderItem.product_id == product_id,
                OrderItem.is_deleted.is_(False),
            )
        )
        item = res.scalar_one_or_none()
        if item:
            item.qty += qty
            return item

        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            qty=qty,
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def set_qty(self, item_id: int, qty: int) -> None:
        item = await self.session.get(OrderItem, item_id)
        item.qty = qty

    async def remove(self, item_id: int) -> None:
        item = await self.session.get(OrderItem, item_id)
        item.is_deleted = True