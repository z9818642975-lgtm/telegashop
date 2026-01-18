# bot/bootstrap/users.py
import os

# bot/bootstrap/users.py
import os





from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.users_dao import UsersDAO


from bot.models.enums import UserRole








def _parse_ids(value: str | None) -> list[int]:


    if not value:


        return []


    return [int(x.strip()) for x in value.split(",") if x.strip()]








async def bootstrap_users(session: AsyncSession) -> None:


    dao = UsersDAO(session)





    admin_id = os.getenv("ADMIN_ID")


    operator_ids = os.getenv("OPERATOR_IDS")





    async with session.begin():


        if admin_id:


            await dao.upsert(int(admin_id), UserRole.ADMIN)





        for op_id in _parse_ids(operator_ids):


            await dao.upsert(op_id, UserRole.OPERATOR)





