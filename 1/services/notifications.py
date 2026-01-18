from aiogram import Bot

class NotificationService:
    @staticmethod
    async def notify_client(bot: Bot, client_id: int, text: str):
        await bot.send_message(chat_id=client_id, text=text)

    @staticmethod
    async def notify_admin(bot: Bot, admin_id: int, text: str):
        await bot.send_message(chat_id=admin_id, text=text)

