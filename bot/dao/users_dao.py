# bot/dao/users_dao.py
from sqlalchemy import select

from bot.dao.base import BaseDAO
from bot.models import User, UserRole


class UsersDAO(BaseDAO):

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        res = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return res.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        tg_id: int,
        role: UserRole = UserRole.CLIENT,
    ) -> User:
        """
        ⬅️ ЭТОТ МЕТОД ЖДЁТ bot/middlewares/user.py
        """
        user = await self.get_by_tg_id(tg_id)
        if user:
            return user

        user = User(
            tg_id=tg_id,
            role=role,
            is_active=True,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        return user

    async def get_or_create_by_tg_id(
        self,
        tg_id: int,
        role: UserRole = UserRole.CLIENT,
    ) -> User:
        """
        Алиас для bootstrap / legacy-кода
        """
        return await self.get_or_create(tg_id=tg_id, role=role)

    async def toggle_active(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            return

        user.is_active = not user.is_active
        await self.session.commit()
