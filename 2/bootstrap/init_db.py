# bot/bootstrap/init_db.py
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

# 🔑 КРИТИЧНО: загружаем ВСЕ модели, чтобы они попали в Base.metadata
import bot.models  # noqa: F401


logger = logging.getLogger("telegashop")

BASE_DIR = Path(__file__).resolve().parents[2]

SCHEMA_FILE = BASE_DIR / "sql" / "01_schema.sql"
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

    statements = [
        stmt.strip()
        for stmt in sql.split(";")
        if stmt.strip()
    ]

    for stmt in statements:
        await conn.exec_driver_sql(stmt)


async def recreate_order_view(conn):
    await conn.exec_driver_sql("DROP VIEW IF EXISTS order_view")

    await conn.exec_driver_sql(
        """
        CREATE VIEW order_view AS
        SELECT
            o.id AS order_id,
            COUNT(oi.id) AS total_items,
            COUNT(*) FILTER (WHERE oi.status = 'ACCEPTED') AS accepted_items,
            COUNT(*) FILTER (WHERE oi.status = 'PAID')     AS paid_items,
            COUNT(*) FILTER (WHERE oi.status = 'DONE')     AS done_items,
            BOOL_AND(oi.status = 'DONE') AS is_completed,
            MAX(oi.completed_at)         AS completed_at
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        GROUP BY o.id
        """
    )


# ============================================================
# INIT DB (BOOTSTRAP, НЕ INSTALLER)
# ============================================================

async def init_db():
    logger.info("🔧 DB bootstrap started")

    await wait_for_db()

    async with engine.begin() as conn:
        # 1️⃣ Проверка существования базовой схемы
        result = await conn.execute(
            text("SELECT to_regclass('public.users')")
        )
        schema_exists = result.scalar() is not None

        if not schema_exists:
            logger.warning("⚠️ Schema not found → applying 01_schema.sql")
            await exec_sql_file(conn, SCHEMA_FILE)
        else:
            logger.info("✅ Schema exists → skipping schema.sql")

        # 2️⃣ Seed — только если products пустая
        try:
            result = await conn.execute(
                text("SELECT COUNT(*) FROM products")
            )
            count = result.scalar() or 0
        except Exception:
            count = 0

        if count == 0:
            logger.info("🌱 Applying seed.sql")
            await exec_sql_file(conn, SEED_FILE)
        else:
            logger.info("🌱 Seed skipped (data exists)")

        # 3️⃣ View можно пересоздавать всегда
        logger.info("👁 Recreating order_view")
        await recreate_order_view(conn)

        # 4️⃣ 🔑 ДОСОЗДАНИЕ ВСЕХ НЕДОСТАЮЩИХ ТАБЛИЦ
        # schema.sql — не покрывает новые модели (OperatorShift и др.)
        await conn.run_sync(Base.metadata.create_all)

    # ============================================================
    # 5️⃣ ADMIN FROM .env (settings.ADMIN_ID)
    # ============================================================

    admin_tg_id = getattr(settings, "ADMIN_ID", None)

    if admin_tg_id:
        async with async_session_maker() as session:
            users_dao = UsersDAO(session)

            admin = await users_dao.get_by_tg_id(admin_tg_id)

            if admin:
                if admin.role != UserRole.ADMIN:
                    admin.role = UserRole.ADMIN
                    await session.commit()
                    logger.info(f"👑 Promoted user {admin_tg_id} to ADMIN")
            else:
                await users_dao.create(
                    tg_id=admin_tg_id,
                    role=UserRole.ADMIN,
                )
                logger.info(f"👑 Created ADMIN user {admin_tg_id}")

    logger.info("✅ DB bootstrap completed")

