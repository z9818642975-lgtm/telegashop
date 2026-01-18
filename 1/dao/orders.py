from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.order import Order
from bot.models.order_item import OrderItem

class OrdersDAO:
    @staticmethod
    async def get_draft(session: AsyncSession, client_id: int) -> Order:
        result = await session.execute(
            select(Order).where(
                order.client_id == client_id,
                Order.status == "DRAFT",
            )
        )
        order = result.scalar_one_or_none()
        if order:
            return order

        order = Order(client_id=client_id, status="DRAFT")
        session.add(order)
        await session.flush()
        return order

    @staticmethod
    async def add_item(session: AsyncSession, order: Order, product_id: int):
        item = OrderItem(order_id=order.id, product_id=product_id, qty=1)
        session.add(item)

    @staticmethod
    async def submit(session: AsyncSession, order: Order, receipt_id: str):
        order.status = "PAID_PENDING"
        order.receipt_id = receipt_id

