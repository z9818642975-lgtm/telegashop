from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User
from bot.models.enums import UserRole


class UsersDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ============================================================
    # GET
    # ============================================================

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()

    # ============================================================
    # CREATE
    # ============================================================

    async def create(
        self,
        *,
        tg_id: int,
        role: UserRole = UserRole.CLIENT,
        is_active: bool = True,
        username: str | None = None,
    ) -> User:
        user = User(
            tg_id=tg_id,
            role=role,
            is_active=is_active,
            username=username,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    # ============================================================
    # USED BY EnsureUserMiddleware
    # ============================================================

    async def get_or_create_by_tg_id(
        self,
        *,
        tg_id: int,
        username: str | None = None,
    ) -> User:
        user = await self.get_by_tg_id(tg_id)
        if user:
            return user

        return await self.create(
            tg_id=tg_id,
            role=UserRole.CLIENT,
            is_active=True,
            username=username,
        )
        

    async def list_operators(self):
        res = await self.session.execute(
            select(User).where(User.role == UserRole.OPERATOR)
        )
        return list(res.scalars().all())

