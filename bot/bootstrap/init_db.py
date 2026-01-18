from __future__ import annotations

import asyncio
import logging
import socket
from pathlib import Path

from sqlalchemy import text

from bot.db import engine, async_session_maker, Base
from bot.config import settings
from bot.dao.users_dao import UsersDAO
from bot.models.enums import UserRole
from bot.bootstrap.users import bootstrap_users

import bot.models  # noqa: F401

logger = logging.getLogger("telegashop")

BASE_DIR = Path(__file__).resolve().parents[2]
SEED_FILE = BASE_DIR / "sql" / "02_seed.sql"


# ============================================================
# UTILS
# ============================================================

async def wait_for_db(
    host: str = "postgres",
    port: int = 5432,
    retries: int = 60,
    delay: float = 1.5,
):
    for attempt in range(1, retries + 1):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            writer.close()
            await writer.wait_closed()
            logger.info(f"✅ Postgres available (attempt {attempt})")
            return
        except (OSError, socket.gaierror):
            logger.info(f"⏳ Waiting for Postgres ({attempt}/{retries})...")
            await asyncio.sleep(delay)

    raise RuntimeError("Postgres is not available")


async def exec_sql_file(conn, path: Path):
    if not path.exists():
        logger.warning(f"⚠️ SQL file not found: {path}")
        return

    sql = path.read_text(encoding="utf-8")
    for stmt in filter(None, map(str.strip, sql.split(";"))):
        await conn.exec_driver_sql(stmt)


async def recreate_order_cart_view(conn):
    await conn.exec_driver_sql("DROP VIEW IF EXISTS order_cart_view")
    await conn.exec_driver_sql(
        """
        CREATE VIEW order_cart_view AS
        SELECT
            o.id AS order_id,
            o.client_id,
            COUNT(oi.id) AS total_items,
            COUNT(*) FILTER (WHERE oi.status = 'ACCEPTED') AS accepted_items,
            COUNT(*) FILTER (WHERE oi.status = 'PAID')     AS paid_items,
            COUNT(*) FILTER (WHERE oi.status = 'DONE')     AS done_items,
            BOOL_AND(oi.status = 'DONE') AS is_completed
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        GROUP BY o.id, o.client_id
        """
    )


# ============================================================
# INIT DB
# ============================================================

async def init_db() -> None:
    logger.info("🔧 DB bootstrap started")

    await wait_for_db()

    async with engine.begin() as conn:
        result = await conn.execute(
            text("SELECT to_regclass('public.users')")
        )
        if result.scalar() is None:
            logger.warning("⚠️ Schema not found → bootstrap disabled")
            return

        logger.info("✅ Schema exists")

        result = await conn.execute(text("SELECT COUNT(*) FROM products"))
        if (result.scalar() or 0) == 0:
            logger.info("🌱 Applying seed.sql")
            await exec_sql_file(conn, SEED_FILE)
        else:
            logger.info("🌱 Seed skipped (data exists)")

        logger.info("👁 Recreating order_cart_view")
        await recreate_order_cart_view(conn)

        await conn.run_sync(Base.metadata.create_all)

    # 👥 USERS / OPERATORS / ADMIN
    async with async_session_maker() as session:
        await bootstrap_users(session)
        await session.commit()

        admin_tg_id = getattr(settings, "ADMIN_ID", None)
        if admin_tg_id:
            users_dao = UsersDAO(session)
            admin = await users_dao.get_by_tg_id(admin_tg_id)

            if admin:
                if admin.role != UserRole.ADMIN:
                    admin.role = UserRole.ADMIN
                    await session.commit()
                    logger.info("👑 Admin promoted")
            else:
                await users_dao.create(
                    tg_id=admin_tg_id,
                    role=UserRole.ADMIN,
                )
                await session.commit()
                logger.info("👑 Admin created")

    logger.info("✅ DB bootstrap completed")
