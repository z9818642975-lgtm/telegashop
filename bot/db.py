# bot/db.py

# bot/db.py


import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.config import settings

logger = logging.getLogger("telegashop")





# =========================


# Engine & Session factory


# =========================





engine: AsyncEngine = create_async_engine(


    settings.DATABASE_URL,


    echo=False,


    pool_pre_ping=True,


)





async_session_factory = async_sessionmaker(


    engine,


    class_=AsyncSession,


    expire_on_commit=False,


)





# 🔑 alias для middleware / services / dao


async_session = async_session_factory





# =========================


# SQL bootstrap helpers


# =========================





SQL_DIR = Path("/app/sql")





SCHEMA_SQL = SQL_DIR / "schema.sql"


SEED_SQL = SQL_DIR / "seed.sql"


ORDER_VIEW_SQL = SQL_DIR / "order_view.sql"








async def _exec_sql_file(path: Path):


    if not path.exists():


        logger.warning(f"⚠️ SQL file not found: {path.name}")


        return





    sql = path.read_text(encoding="utf-8")





    async with engine.begin() as conn:


        await conn.execute(text(sql))








async def _has_products() -> bool:


    async with async_session_factory() as session:


        result = await session.execute(


            text("SELECT COUNT(*) FROM products")


        )


        return result.scalar_one() > 0








# =========================


# Public bootstrap


# =========================





async def init_db():


    logger.info("🔎 DB bootstrap started")





    # schema.sql


    await _exec_sql_file(SCHEMA_SQL)





    # seed.sql (only if empty)


    if SEED_SQL.exists():


        if not await _has_products():


            logger.info("🌱 No products → applying seed.sql")


            await _exec_sql_file(SEED_SQL)





    # order_view.sql


    if ORDER_VIEW_SQL.exists():


        logger.info("📄 Applying order_view.sql")


        await _exec_sql_file(ORDER_VIEW_SQL)





    logger.info("✅ DB bootstrap finished")






