# bot/services/order_service.py
from sqlalchemy.ext.asyncio import AsyncSession

# bot/services/order_service.py
from sqlalchemy.ext.asyncio import AsyncSession


from bot.dao.orders_dao import OrdersDAO


from bot.models.enums import OrderStatus





class OrderService:


    @staticmethod


    async def checkout_start(order_id: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        if order.status != OrderStatus.NEW:


            raise ValueError("invalid state")


        order.status = OrderStatus.CHECKOUT_DELIVERY_TYPE


        await session.commit()





    @staticmethod


    async def select_pickup(order_id: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.delivery_type = "pickup"


        order.delivery_price = 0


        order.status = OrderStatus.CHECKOUT_PAYMENT_METHOD


        await session.commit()





    @staticmethod


    async def select_delivery(order_id: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.delivery_type = "delivery"


        order.status = OrderStatus.CHECKOUT_DELIVERY_PRICE


        await session.commit()





    @staticmethod


    async def select_delivery_price(order_id: int, price: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.delivery_price = price


        order.status = OrderStatus.CHECKOUT_PAYMENT_METHOD


        await session.commit()





    @staticmethod


    async def select_payment_method(order_id: int, method: str, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.payment_method = method


        order.status = OrderStatus.WAITING_PAYMENT


        await session.commit()





    @staticmethod


    async def submit_payment(order_id: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.status = OrderStatus.PAYMENT_SUBMITTED


        await session.commit()





    @staticmethod


    async def cancel_order(order_id: int, session: AsyncSession):


        order = await OrdersDAO(session).get(order_id)


        order.status = OrderStatus.CANCELLED


        await session.commit()





