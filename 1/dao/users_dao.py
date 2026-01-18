# bot/dao/users_dao.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User
from bot.models.enums import UserRole


class UsersDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================
    # GET
    # =========================================================

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        res = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return res.scalar_one_or_none()

    # =========================================================
    # CREATE
    # =========================================================

    async def create(
        self,
        *,
        tg_id: int,
        username: str | None,
        full_name: str | None,
        role: UserRole = UserRole.CLIENT,
    ) -> User:
        user = User(
            tg_id=tg_id,
            username=username,
            full_name=full_name,
            role=role,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    # =========================================================
    # GET OR CREATE  Р Р†РІР‚В РЎвЂ™ Р В РІР‚в„ўР В РЎвЂ™Р В РІР‚вЂњР В РЎСљР В РЎвЂє
    # =========================================================

    async def get_or_create(self, tg_user) -> User:
        """
        tg_user: aiogram.types.User
        """
        user = await self.get_by_tg_id(tg_user.id)
        if user:
            return user

        return await self.create(
            tg_id=tg_user.id,
            username=tg_user.username,
            full_name=tg_user.full_name,
            role=UserRole.CLIENT,
        )

