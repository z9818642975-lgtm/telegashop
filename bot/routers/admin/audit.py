# bot/routers/admin/audit.py


# bot/routers/admin/audit.py



from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.text_decorations import html_decoration as hd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.models.audit_log import AuditLog

router = Router()





def safe(t: str) -> str:


    return hd.quote(t)





@router.message(RoleFilter("admin"), F.text == "А 🧾 Audit log")


async def view_audit(message: Message, session: AsyncSession):


    res = await session.execute(


        select(AuditLog).order_by(AuditLog.id.desc()).limit(20)


    )


    logs = res.scalars().all()


    text = "🧾 Последние действия:\n\n"


    for log in logs:


        text += f"{log.actor_id}: {log.action} {log.entity} {log.entity_id}\n"


    await message.answer(safe(text), parse_mode="HTML")








