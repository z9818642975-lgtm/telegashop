from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.dao.users_dao import UsersDAO
from bot.models.enums import UserRole


class RoleService:
    @staticmethod
    async def resolve_user(
        *,
        session: AsyncSession,
        tg_id: int,
    ):
        dao = UsersDAO(session)

        # ADMIN из env
        if tg_id in settings.ADMINS or (
            settings.ADMIN_ID and tg_id == settings.ADMIN_ID
        ):
            user = await dao.upsert(tg_id, UserRole.ADMIN)
            return user, UserRole.ADMIN

        # обычный пользователь
        user = await dao.get_or_create_by_tg_id(
            tg_id=tg_id,
            role=UserRole.CLIENT,
        )

        if user.role == UserRole.OPERATOR:
            return user, UserRole.OPERATOR

        return user, UserRole.CLIENT
