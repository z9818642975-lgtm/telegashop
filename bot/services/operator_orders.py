# bot/services/operator_orders.py
from sqlalchemy.ext.asyncio import AsyncSession

# bot/services/operator_orders.py
from bot.dao.operator_orders_dao import OperatorOrdersDAO


class OperatorOrdersService:


    def __init__(self, session: AsyncSession):


        self.dao = OperatorOrdersDAO(session)





    async def list_available(self):


        return await self.dao.list_available()





    async def accept(self, order_item_id: int, operator_id: int):


        return await self.dao.accept(order_item_id, operator_id)







