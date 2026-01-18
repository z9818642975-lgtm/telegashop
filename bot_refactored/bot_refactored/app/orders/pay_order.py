from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class PayOrderUseCase:
    def __init__(self, order_id: int, session: AsyncSession):
        self.order_id = order_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            if order.status == OrderStatus.PAID:
                return

            OrderDomain(order.status).can_transition(OrderStatus.PAID)
            await OrdersDAO.mark_paid(order)

