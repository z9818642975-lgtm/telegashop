from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.salary_dao import SalaryDAO

router = Router(name="operator_salary")


# =========================================================
# СЂСџвЂ™В° Р СљР С›Р Р‡ Р вЂ”Р С’Р В Р СџР вЂєР С’Р СћР С’
# =========================================================
@router.message(RoleFilter("operator"), F.text == "СЂСџвЂ™В° Р вЂ”Р В°РЎР‚Р С—Р В»Р В°РЎвЂљР В°")
async def my_salary(message, *, session: AsyncSession | None = None,
    user,
):
    if not user:
        await message.answer("РІСњРЉ Р СџР С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»РЎРЉ Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…")
        return

    salary_dao = SalaryDAO(session)
    rows = await salary_dao.list_by_operator(user.id)

    if not rows:
        await message.answer("СЂСџвЂ™С‘ Р СњР В°РЎвЂЎР С‘РЎРѓР В»Р ВµР Р…Р С‘Р в„– Р С—Р С•Р С”Р В° Р Р…Р ВµРЎвЂљ")
        return

    total = 0
    text = "СЂСџвЂ™В° <b>Р СљР С•РЎРЏ Р В·Р В°РЎР‚Р С—Р В»Р В°РЎвЂљР В°</b>\n\n"

    for r in rows:
        total += r.amount
        text += (
            f"СЂСџВ§С• Р вЂ”Р В°Р С”Р В°Р В·: {r.order_id or 'РІР‚вЂќ'}\n"
            f"СЂСџвЂ™Вµ Р РЋРЎС“Р СР СР В°: {r.amount} РІвЂљР…\n"
            f"СЂСџвЂњРЉ Р РЋРЎвЂљР В°РЎвЂљРЎС“РЎРѓ: {r.status}\n"
            f"РІРЏВ± {r.created_at:%d.%m %H:%M}\n\n"
        )

    text += f"<b>Р ВРЎвЂљР С•Р С–Р С• Р С” Р Р†РЎвЂ№Р С—Р В»Р В°РЎвЂљР Вµ:</b> {total} РІвЂљР…"

    await message.answer(text)


# =========================================================
# СЂСџвЂњВ¤ Р вЂ”Р С’Р СџР В Р С›Р РЋР ВР СћР В¬ Р вЂ™Р В«Р СџР вЂєР С’Р СћР Р€
# =========================================================
@router.message(RoleFilter("operator"), F.text == "СЂСџвЂњВ¤ Р вЂ”Р В°Р С—РЎР‚Р С•РЎРѓР С‘РЎвЂљРЎРЉ Р Р†РЎвЂ№Р С—Р В»Р В°РЎвЂљРЎС“")
async def request_payout(message, *, session: AsyncSession | None = None,
    user,
):
    if not user:
        await message.answer("РІСњРЉ Р СџР С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»РЎРЉ Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…")
        return

    salary_dao = SalaryDAO(session)
    await salary_dao.request_payout(user.id)
    await session.commit()

    await message.answer("СЂСџвЂњВ¤ Р вЂ”Р В°Р С—РЎР‚Р С•РЎРѓ Р Р…Р В° Р Р†РЎвЂ№Р С—Р В»Р В°РЎвЂљРЎС“ Р С•РЎвЂљР С—РЎР‚Р В°Р Р†Р В»Р ВµР Р…")



