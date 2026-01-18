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


        Р вЂўР Т‘Р С‘Р Р…Р В°РЎРЏ РЎвЂљР С•РЎвЂЎР С”Р В° Р С•Р С—РЎР‚Р ВµР Т‘Р ВµР В»Р ВµР Р…Р С‘РЎРЏ Р С—Р С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»РЎРЏ Р С‘ РЎР‚Р С•Р В»Р С‘.


        Р СџРЎР‚Р С‘Р С•РЎР‚Р С‘РЎвЂљР ВµРЎвЂљ:


        1. ADMIN (env)


        2. OPERATOR (Р С‘Р В· Р вЂР вЂќ)


        3. CLIENT (default)


        """





        # 1РїС‘РЏРІС“Р€ Р вЂ“РЎвЂРЎРѓРЎвЂљР С”Р С‘Р в„– ADMIN Р С‘Р В· env


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





        # 2РїС‘РЏРІС“Р€ Р СџР С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»РЎРЉ Р С‘Р В· Р вЂР вЂќ


        user = await UsersDAO.get_or_create(


            session=session,


            tg_id=tg_id,


            username=username,


            role=UserRole.CLIENT,


        )





        # 3РїС‘РЏРІС“Р€ Р В Р С•Р В»РЎРЉ Р С‘Р В· Р вЂР вЂќ (Р ВµРЎРѓР В»Р С‘ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р Р…Р В°Р В·Р Р…Р В°РЎвЂЎР ВµР Р…)


        if user.role == UserRole.OPERATOR:


            return user, UserRole.OPERATOR





        # 4РїС‘РЏРІС“Р€ Default


        return user, UserRole.CLIENT





