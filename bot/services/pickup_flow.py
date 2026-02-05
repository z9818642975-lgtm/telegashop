# bot/services/pickup_flow.py
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.enums import OrderItemStatus

# bot/services/pickup_flow.py
from bot.models.order_item import OrderItem


class PickupService:


    def __init__(self, session: AsyncSession):


        self.session = session





    async def mark_wait(self, item: OrderItem):


        # статус не меняем — только событие


        # сюда можно добавить notify оператору


        pass





    async def mark_done(self, item: OrderItem):


        item.status = OrderItemStatus.DONE


        await self.session.commit()







