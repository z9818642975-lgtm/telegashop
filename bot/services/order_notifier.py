# bot/services/order_notifier.py
from aiogram import Bot

from bot.models.enums import OrderItemStatus

# bot/services/order_notifier.py
from bot.models.order_item import OrderItem


class OrderNotifier:


    def __init__(self, bot: Bot):


        self.bot = bot





    async def notify_client(self, item: OrderItem):


        client_id = item.order.client_id





        messages = {


            OrderItemStatus.ACCEPTED: "✅ Заказ принят оператором",


            OrderItemStatus.PAID: "💳 Оплата подтверждена",


            OrderItemStatus.READY: "📦 Заказ готов к выдаче",


            OrderItemStatus.DONE: "🏁 Заказ завершён",


        }





        text = messages.get(item.status)


        if text:


            await self.bot.send_message(client_id, text)







