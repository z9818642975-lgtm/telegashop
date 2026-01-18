# bot/services/pickup_flow.py
from sqlalchemy.ext.asyncio import AsyncSession

# bot/services/pickup_flow.py
from sqlalchemy.ext.asyncio import AsyncSession


from bot.models.order_item import OrderItem


from bot.models.enums import OrderItemStatus








class PickupService:


    def __init__(self, session: AsyncSession):


        self.session = session





    async def mark_wait(self, item: OrderItem):


        # РЎРѓРЎвЂљР В°РЎвЂљРЎС“РЎРѓ Р Р…Р Вµ Р СР ВµР Р…РЎРЏР ВµР С РІР‚вЂќ РЎвЂљР С•Р В»РЎРЉР С”Р С• РЎРѓР С•Р В±РЎвЂ№РЎвЂљР С‘Р Вµ


        # РЎРѓРЎР‹Р Т‘Р В° Р СР С•Р В¶Р Р…Р С• Р Т‘Р С•Р В±Р В°Р Р†Р С‘РЎвЂљРЎРЉ notify Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎС“


        pass





    async def mark_done(self, item: OrderItem):


        item.status = OrderItemStatus.DONE


        await self.session.commit()





