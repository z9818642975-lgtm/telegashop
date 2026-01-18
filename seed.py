from __future__ import annotations

import asyncio
import socket
from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.core.config import settings
from bot.core.logger import logger

from bot.models.user import User, UserRole
from bot.models.product import Product
from bot.models.warehouse import Warehouse
from bot.models.bank_account import BankAccount


# ============================================================
# DATA
# ============================================================

USERS = [
    dict(
        tg_id=7444294101,
        username="admin",
        full_name="Main Admin",
        role=UserRole.ADMIN,
    ),
    dict(
        tg_id=8413852743,
        username="operator",
        full_name="Main Operator",
        role=UserRole.OPERATOR,
    ),
]

PRODUCTS = [
    dict(title="?? Ìÿó", base_price=3500, min_qty=1,
         description="1 øò = 3500?, îò 2 øò = 3000?/øò"),
    dict(title="?? Êîê", base_price=11000, min_qty=1,
         description="1 øò = 11000?, îò 2 øò = 10000?/øò"),
    dict(title="?? Ýêñ", base_price=1500, min_qty=2,
         description="Ïðîäà¸òñÿ îò 2 øò"),
    dict(title="?? Ãàð", base_price=1800, min_qty=1),
    dict(title="?? Áîø", base_price=1800, min_qty=1),
    dict(title="?? Ëèð", base_price=4000, min_qty=1),
]

WAREHOUSES = [
    dict(title="Ãëàâíûé ñêëàä", address=None),
    dict(title="Ñåâåðíûé ñêëàä", address=None),
    dict(title="Þæíûé ñêëàä", address=None),
]

BANK_ACCOUNTS: List[Tuple[str, str]] = [
    ("Ð¡Ð±ÐµÑ€Ð±Ð°Ð½Ðº", "2202208208297771"),
    ("Ð¡Ð±ÐµÑ€Ð±Ð°Ð½Ðº", "4276550062549103"),
    ("Ð¡Ð±ÐµÑ€Ð±Ð°Ð½Ðº", "9817815379"),   # SBP
    ("Ð¡Ð±ÐµÑ€Ð±Ð°Ð½Ðº", "9818642975"),   # SBP
    ("Ð¢-Ð‘Ð°Ð½Ðº", "9818642975"),
    ("Ð¢-Ð‘Ð°Ð½Ðº", "2200700988565783"),
    ("ÐÐ»ÑŒÑ„Ð°-Ð‘Ð°Ð½Ðº", "2200152314652077"),
    ("ÐÐ»ÑŒÑ„Ð°-Ð‘Ð°Ð½Ðº", "9818642975"),
]


# ============================================================
# HELPERS
# ============================================================

def _parse_pg_host(db_url: str) -> tuple[str, int]:
    host, port = "postgres", 5432
    try:
        after_at = db_url.split("@", 1)[1]
        host_port = after_at.split("/", 1)[0]
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
    except Exception:
        pass
    return host, port


async def wait_pg(timeout: int = 30):
    host, port = _parse_pg_host(settings.DATABASE_URL)
    logger.info("â³ Waiting for PostgreSQL %s:%s", host, port)

    for _ in range(timeout * 10):
        try:
            with socket.create_connection((host, port), timeout=0.3):
                logger.info("âœ… PostgreSQL ready")
                return
        except OSError:
            await asyncio.sleep(0.1)

    raise RuntimeError("PostgreSQL not available")


def is_sbp(value: str) -> bool:
    digits = "".join(c for c in value if c.isdigit())
    return len(digits) <= 11


def mask_card(value: str) -> str:
    d = "".join(c for c in value if c.isdigit())
    if len(d) < 8:
        return d
    return f"{d[:4]} **** **** {d[-4:]}"


# ============================================================
# SEED
# ============================================================

async def seed():
    await wait_pg()

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as session:
        logger.info("ðŸŒ± START DB SEED")

        # ---------------- USERS ----------------
        for u in USERS:
            exists = await session.scalar(
                select(User).where(User.tg_id == u["tg_id"])
            )
            if not exists:
                session.add(User(
                    tg_id=u["tg_id"],
                    username=u["username"],
                    full_name=u["full_name"],
                    role=u["role"],
                ))
                logger.info("ðŸ‘¤ User seeded: %s", u["tg_id"])

        # ---------------- PRODUCTS ----------------
        for p in PRODUCTS:
            exists = await session.scalar(
                select(Product).where(Product.title == p["title"])
            )
            if not exists:
                session.add(Product(
                    title=p["title"],
                    description=p.get("description"),
                    base_price=p["base_price"],
                    min_qty=p["min_qty"],
                    is_active=True,
                ))
                logger.info("ðŸ“¦ Product seeded: %s", p["title"])

        # ---------------- WAREHOUSES ----------------
        for w in WAREHOUSES:
            exists = await session.scalar(
                select(Warehouse).where(Warehouse.title == w["title"])
            )
            if not exists:
                session.add(Warehouse(
                    title=w["title"],
                    address=w.get("address"),
                    is_active=True,
                ))
                logger.info("ðŸ¬ Warehouse seeded: %s", w["title"])

        # ---------------- BANK ACCOUNTS ----------------
        for bank_name, value in BANK_ACCOUNTS:
            sbp_phone = value if is_sbp(value) else None
            card_number = None if sbp_phone else value
            card_masked = mask_card(value) if card_number else None

            exists = await session.scalar(
                select(BankAccount).where(
                    BankAccount.bank_name == bank_name,
                    BankAccount.card_number == card_number,
                    BankAccount.sbp_phone == sbp_phone,
                )
            )

            if not exists:
                session.add(BankAccount(
                    bank_name=bank_name,
                    card_number=card_number,
                    card_masked=card_masked,
                    sbp_phone=sbp_phone,
                    is_active=True,
                    load=0,
                    weight=100,
                ))
                logger.info("ðŸ¦ BankAccount seeded: %s %s", bank_name, value)

        await session.commit()
        logger.info("âœ… DB SEED DONE")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())

