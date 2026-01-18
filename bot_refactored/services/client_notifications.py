from aiogram import Bot

async def notify_client(bot: Bot, client_id: int, text: str):
    await bot.send_message(client_id, text)

