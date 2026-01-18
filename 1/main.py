from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.routers import router as root_router

from bot.db.session import async_session_maker
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.user import UserMiddleware
from bot.middlewares.antispam import AntiSpamMiddleware


async def main() -> None:
    # --------------------------------------------------
    # LOGGING
    # --------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s",
    )
    logging.info("🚀 Starting bot")

    # --------------------------------------------------
    # BOT
    # --------------------------------------------------
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # --------------------------------------------------
    # DISPATCHER
    # --------------------------------------------------
    dp = Dispatcher()

    # --------------------------------------------------
    # MIDDLEWARES (ORDER IS IMPORTANT)
    # --------------------------------------------------
    dp.update.middleware(DbSessionMiddleware(async_session_maker))
    dp.update.middleware(UserMiddleware())
    dp.update.middleware(AntiSpamMiddleware())

    # --------------------------------------------------
    # ROUTERS
    # --------------------------------------------------
    dp.include_router(root_router)

    # --------------------------------------------------
    # START
    # --------------------------------------------------
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

