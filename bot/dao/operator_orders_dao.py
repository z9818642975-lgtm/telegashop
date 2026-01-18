# bot/dao/operator_orders_dao.py
from sqlalchemy import select, update

# bot/dao/operator_orders_dao.py
from sqlalchemy import select, update


from sqlalchemy.ext.asyncio import AsyncSession





from bot.models.order_item import OrderItem, OrderItemStatus








class OperatorOrdersDAO:


    def __init__(self, session: AsyncSession):


        self.session = session





    async def list_available(self):


        res = await self.session.execute(


            select(OrderItem).where(


                OrderItem.status == OrderItemStatus.NEW


            )


        )


        return res.scalars().all()





    async def accept(self, order_item_id: int, operator_id: int):


        await self.session.execute(


            update(OrderItem)


            .where(OrderItem.id == order_item_id)


            .values(


                status=OrderItemStatus.ACCEPTED,


                operator_id=operator_id,


            )


        )


        await self.session.flush()





