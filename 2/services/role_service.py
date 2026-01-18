# bot/services/role_service.py
from sqlalchemy.ext.asyncio import AsyncSession

# bot/services/role_service.py
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


        username: str | None,


    ):


        """


        Единая точка определения пользователя и роли.


        Приоритет:


        1. ADMIN (env)


        2. OPERATOR (из БД)


        3. CLIENT (default)


        """





        # 1️⃣ Жёсткий ADMIN из env


        if tg_id in settings.ADMINS or (


            settings.ADMIN_ID and tg_id == settings.ADMIN_ID


        ):


            user = await UsersDAO.get_or_create(


                session=session,


                tg_id=tg_id,


                username=username,


                role=UserRole.ADMIN,


            )


            return user, UserRole.ADMIN





        # 2️⃣ Пользователь из БД


        user = await UsersDAO.get_or_create(


            session=session,


            tg_id=tg_id,


            username=username,


            role=UserRole.CLIENT,


        )





        # 3️⃣ Роль из БД (если оператор назначен)


        if user.role == UserRole.OPERATOR:


            return user, UserRole.OPERATOR





        # 4️⃣ Default


        return user, UserRole.CLIENT





