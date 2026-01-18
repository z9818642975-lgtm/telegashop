from aiogram import Bot

async def notify(bot: Bot, client_id: int, text: str):
    await bot.send_message(client_id, text)

