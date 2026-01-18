# bot/dao/orders_dao.py
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.models.order import Order
from bot.models.order_item import OrderItem
from bot.models.enums import OrderStatus


class OrdersDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================
    # CART (OrderStatus.NEW)
    # =========================================================

    async def get_cart(self, client_id: int) -> Order | None:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items)
                .selectinload(OrderItem.product)
            )
            .where(
                Order.client_id == client_id,
                Order.status == OrderStatus.NEW,
            )
            .limit(1)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_or_create_cart(self, client_id: int) -> Order:
        order = await self.get_cart(client_id)
        if order:
            return order

        order = Order(
            client_id=client_id,
            status=OrderStatus.NEW,
        )
        self.session.add(order)
        await self.session.flush()
        return order

    async def clear_cart(self, client_id: int) -> None:
        order = await self.get_cart(client_id)
        if not order:
            return

        await self.session.execute(
            delete(OrderItem).where(
                OrderItem.order_id == order.id
            )
        )
        await self.session.flush()

    # =========================================================
    # ADD PRODUCT (IDEMPOTENT)
    # =========================================================

    async def add_product(
        self,
        *,
        user_id: int,
        product_id: int,
        qty: int = 1,
    ) -> OrderItem:
        """
        Идемпотентное добавление товара в корзину.

        - если OrderItem уже есть → вернуть его
        - qty НЕ увеличивается
        - qty меняется ТОЛЬКО через item:qty
        """

        order = await self.get_or_create_cart(user_id)

        res = await self.session.execute(
            select(OrderItem).where(
                OrderItem.order_id == order.id,
                OrderItem.product_id == product_id,
            )
        )
        item = res.scalar_one_or_none()

        if item:
            return item

        item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            qty=qty,
            price=item.product.base_price
            if hasattr(item := None, "product") else None,
        )

        # ↑ если price у тебя проставляется иначе —
        # оставь СВОЮ логику, это не влияет на идемпотентность

        self.session.add(item)
        await self.session.flush()
        return item

    # =========================================================
    # STATUS
    # =========================================================

    async def set_status(
        self,
        order_id: int,
        status: OrderStatus,
    ) -> None:
        res = await self.session.execute(
            select(Order).where(Order.id == order_id)
        )
        order = res.scalar_one()
        order.status = status
        await self.session.flush()
