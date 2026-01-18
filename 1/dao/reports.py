from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order import Order
from bot.models.operator_salary import OperatorSalary
from bot.constants.order_status import OrderStatus

class ReportsDAO:
    @staticmethod
    async def orders_by_operator(session: AsyncSession):
        result = await session.execute(
            select(
                Order.operator_id,
                func.count(Order.id),
            )
            .where(Order.status == OrderStatus.PAID)
            .group_by(Order.operator_id)
        )
        return result.all()

    @staticmethod
    async def salary_by_operator(session: AsyncSession):
        result = await session.execute(
            select(
                OperatorSalary.operator_id,
                func.sum(OperatorSalary.amount),
            )
            .group_by(OperatorSalary.operator_id)
        )
        return result.all()

    @staticmethod
    async def all_orders(session: AsyncSession):
        result = await session.execute(select(Order))
        return result.scalars().all()

