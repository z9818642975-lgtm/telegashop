# bot/bootstrap/users.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.dao.users_dao import UsersDAO
from bot.models.enums import UserRole


async def bootstrap_users(session: AsyncSession) -> None:
    """
    Bootstrap пользователей из ENV.

    Правила:
    - ADMIN_ID → всегда ADMIN
    - ADMINS → ADMIN
    - OPERATORS → OPERATOR
    - роли назначаются ТОЛЬКО по tg_id
    """

    dao = UsersDAO(session)

    # =========================================================
    # ADMIN_ID (один, приоритетный)
    # =========================================================
    if settings.ADMIN_ID:
        await dao.get_or_create_by_tg_id(
            tg_id=settings.ADMIN_ID,
            role=UserRole.ADMIN,
        )

    # =========================================================
    # ADMINS (список)
    # =========================================================
    for tg_id in settings.ADMINS:
        await dao.get_or_create_by_tg_id(
            tg_id=tg_id,
            role=UserRole.ADMIN,
        )

    # =========================================================
    # OPERATORS (список)
    # =========================================================
    for tg_id in settings.OPERATORS:
        await dao.get_or_create_by_tg_id(
            tg_id=tg_id,
            role=UserRole.OPERATOR,
        )


