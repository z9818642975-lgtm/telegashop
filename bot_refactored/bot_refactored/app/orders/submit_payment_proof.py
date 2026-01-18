from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class SubmitPaymentProofUseCase:
    def __init__(
        self,
        *,
        order_id: int,
        client_id: int,
        photo_id: str,
        comment: str | None,
        session: AsyncSession,
    ):
        self.order_id = order_id
        self.client_id = client_id
        self.photo_id = photo_id
        self.comment = comment
        self.session = session

    async def execute(self) -> None:
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(
                self.session,
                self.order_id,
            )
            if not order:
                raise ValueError("order not found")

            if order.client_id != self.client_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(
                OrderStatus.WAITING_CONFIRMATION
            )

            order.payment_photo_id = self.photo_id
            order.payment_comment = self.comment
            order.status = OrderStatus.WAITING_CONFIRMATION

