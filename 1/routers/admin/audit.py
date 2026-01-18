# bot/routers/admin/audit.py


# bot/routers/admin/audit.py



from aiogram import Router, F


from aiogram.types import Message


from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select


from aiogram.utils.text_decorations import html_decoration as hd





from bot.filters.role import RoleFilter


from bot.models.audit_log import AuditLog





router = Router()





def safe(t: str) -> str:


    return hd.quote(t)





# ❌ DISABLED (admin/operator text handler)
async def view_audit(message, *, session: AsyncSession | None = None):


    res = await session.execute(


        select(AuditLog).order_by(AuditLog.id.desc()).limit(20)


    )


    logs = res.scalars().all()


    text = "РЎР‚РЎСџР’В§РЎвЂў Р В РЎСџР В РЎвЂўР РЋР С“Р В Р’В»Р В Р’ВµР В РўвЂР В Р вЂ¦Р В РЎвЂР В Р’Вµ Р В РўвЂР В Р’ВµР В РІвЂћвЂ“Р РЋР С“Р РЋРІР‚С™Р В Р вЂ Р В РЎвЂР РЋР РЏ:\n\n"


    for l in logs:


        text += f"{l.actor_id}: {l.action} {l.entity} {l.entity_id}\n"


    await message.answer(safe(text), parse_mode="HTML")







