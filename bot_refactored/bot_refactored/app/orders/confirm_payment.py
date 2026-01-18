from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class ConfirmPaymentUseCase:
    def __init__(
        self,
        *,
        order_id: int,
        operator_id: int,
        session: AsyncSession,
    ):
        self.order_id = order_id
        self.operator_id = operator_id
        self.session = session

    async def execute(self) -> None:
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(
                self.session,
                self.order_id,
            )
            if not order:
                raise ValueError("order not found")

            if order.operator_id != self.operator_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(
                OrderStatus.PAID
            )

            order.status = OrderStatus.PAID

