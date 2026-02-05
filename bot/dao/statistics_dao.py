# bot/dao/statistics_dao.py
from sqlalchemy import func, select

from bot.dao.base import BaseDAO
from bot.models import OperatorShift, Order, OrderStatus


class StatisticsDAO(BaseDAO):

    async def revenue_total(self) -> int:
        res = await self.session.execute(
            select(func.sum(Order.total_price))
            .where(Order.status == OrderStatus.DONE)
        )
        return res.scalar() or 0

    async def orders_by_operator(self):
        res = await self.session.execute(
            select(
                OperatorShift.operator_id,
                func.count(Order.id),
            )
            .join(Order, Order.operator_id == OperatorShift.operator_id)
            .where(Order.status == OrderStatus.DONE)
            .group_by(OperatorShift.operator_id)
        )
        return res.all()
