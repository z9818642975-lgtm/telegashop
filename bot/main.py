# bot/main.py
# bot/main.py

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.bootstrap.init_db import init_db
from bot.config import settings
from bot.db import async_session_maker
from bot.middlewares.db import DBSessionMiddleware
from bot.middlewares.role import RoleMiddleware
from bot.middlewares.user import EnsureUserMiddleware
from bot.routers import router as root_router
from bot.services.operator_shift_watcher import operator_shift_watcher

# ------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("telegashop")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

async def main() -> None:
    logger.info("🚀 Bot starting")

    # 🔧 DB bootstrap
    await init_db()

    # 🤖 Bot
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # 📦 Dispatcher
    dp = Dispatcher()

    # --------------------------------------------------------
    # MIDDLEWARES (ORDER IS CRITICAL)
    # --------------------------------------------------------
    dp.update.middleware(DBSessionMiddleware(async_session_maker))
    dp.update.middleware(EnsureUserMiddleware())
    dp.update.middleware(RoleMiddleware())

    # --------------------------------------------------------
    # ROUTERS (ALL ROUTERS COME FROM root_router)
    # --------------------------------------------------------
    dp.include_router(root_router)

    # --------------------------------------------------------
    # BACKGROUND TASKS
    # --------------------------------------------------------
    asyncio.create_task(
        operator_shift_watcher(
            bot=bot,
            sessionmaker=async_session_maker,
        )
    )

    logger.info("✅ Bot started")

    # ▶️ Polling
    await dp.start_polling(bot)


# ------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())

# ============================================================
# OPERATOR ROUTERS (ORDER IS CRITICAL)
# ============================================================
