# bot/services/order_notifier.py
from aiogram import Bot

# bot/services/order_notifier.py
from aiogram import Bot


from bot.models.order_item import OrderItem


from bot.models.enums import OrderItemStatus








class OrderNotifier:


    def __init__(self, bot: Bot):


        self.bot = bot





    async def notify_client(self, item: OrderItem):


        client_id = item.order.client_id





        messages = {


            OrderItemStatus.ACCEPTED: "РІСљвЂ¦ Р вЂ”Р В°Р С”Р В°Р В· Р С—РЎР‚Р С‘Р Р…РЎРЏРЎвЂљ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р С•Р С",


            OrderItemStatus.PAID: "СЂСџвЂ™С– Р С›Р С—Р В»Р В°РЎвЂљР В° Р С—Р С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘Р ВµР Р…Р В°",


            OrderItemStatus.READY: "СЂСџвЂњВ¦ Р вЂ”Р В°Р С”Р В°Р В· Р С–Р С•РЎвЂљР С•Р Р† Р С” Р Р†РЎвЂ№Р Т‘Р В°РЎвЂЎР Вµ",


            OrderItemStatus.DONE: "СЂСџРЏРѓ Р вЂ”Р В°Р С”Р В°Р В· Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬РЎвЂР Р…",


        }





        text = messages.get(item.status)


        if text:


            await self.bot.send_message(client_id, text)





