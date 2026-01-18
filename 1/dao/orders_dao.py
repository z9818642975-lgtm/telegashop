from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order import Order, OrderStatus
from bot.models.order_item import OrderItem
from bot.models.user import User


class OrdersDAO:
    # =========================================================
    # CART
    # =========================================================

    @staticmethod
    async def get_cart(
        session: AsyncSession,
        client_id: int,  # РІвЂ С’ users.id
    ) -> Order | None:
        res = await session.execute(
            select(Order).where(
                order.client_id == client_id,
                Order.status == OrderStatus.NEW,
            )
        )
        return res.scalar_one_or_none()

    @staticmethod
    async def get_or_create_cart(
        session: AsyncSession,
        user: User,  # РІвЂ С’ Р вЂ™Р РЋР вЂўР вЂњР вЂќР С’ User
    ) -> Order:
        order = await OrdersDAO.get_cart(session, user.id)
        if order:
            return order

        order = Order(
            client_id=user.id,
            status=OrderStatus.NEW,
        )
        session.add(order)
        await session.flush()
        return order

    # =========================================================
    # ITEMS
    # =========================================================

    @staticmethod
    async def add_item(
        session: AsyncSession,
        order_id: int,
        product_id: int,
        qty: int,
    ):
        res = await session.execute(
            select(OrderItem).where(
                OrderItem.order_id == order_id,
                OrderItem.product_id == product_id,
            )
        )
        item = res.scalar_one_or_none()

        if item:
            item.quantity += qty
        else:
            session.add(
                OrderItem(
                    order_id=order_id,
                    product_id=product_id,
                    quantity=qty,
                )
            )

        await session.flush()

    @staticmethod
    async def set_quantity(
        session: AsyncSession,
        item_id: int,
        qty: int,
    ):
        res = await session.execute(
            select(OrderItem).where(OrderItem.id == item_id)
        )
        item = res.scalar_one_or_none()

        if not item:
            return

        if qty <= 0:
            await session.delete(item)
        else:
            item.quantity = qty

        await session.flush()

    @staticmethod
    async def remove_item(
        session: AsyncSession,
        item_id: int,
    ):
        res = await session.execute(
            select(OrderItem).where(OrderItem.id == item_id)
        )
        item = res.scalar_one_or_none()

        if item:
            await session.delete(item)
            await session.flush()

