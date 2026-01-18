from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.order import OrderDomain


class AcceptOrderUseCase:
    def __init__(self, order_id: int, operator_id: int, session: AsyncSession):
        self.order_id = order_id
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            shift = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if not shift:
                raise PermissionError("no active shift")

            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            OrderDomain(order.status).can_transition(order.status.ACCEPTED)  # type: ignore
            await OrdersDAO.accept(order, self.operator_id, shift.id)

