import asyncio
from aiogram import Bot, Dispatcher
from bot.core.config import settings
from bot.core.logger import logger
from bot.web.health import run_health_server
from bot.tasks.operator_online_task import run_online_task
from bot.handlers.client import router as client_router
from bot.handlers.operator import router as operator_router
from bot.handlers.admin import router as admin_router

async def main():
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(client_router)
    dp.include_router(operator_router)
    dp.include_router(admin_router)

    await run_health_server(settings.HEALTH_PORT)
    asyncio.create_task(run_online_task(bot))

    logger.info("🚀 TelegaShop FINAL PROD FULL started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
