# bot/dao/operator_orders_dao.py
from sqlalchemy import select, update

from bot.dao.base import BaseDAO
from bot.models.order_item import OrderItem, OrderItemStatus


class OperatorOrdersDAO(BaseDAO):

    async def list_available(self) -> list[OrderItem]:
        res = await self.session.execute(
            select(OrderItem).where(
                OrderItem.status == OrderItemStatus.NEW
            )
        )
        return list(res.scalars())

    async def accept(self, order_item_id: int, operator_id: int) -> None:
        await self.session.execute(
            update(OrderItem)
            .where(OrderItem.id == order_item_id)
            .values(
                status=OrderItemStatus.ACCEPTED,
                operator_id=operator_id,
            )
        )
        await self.session.flush()
