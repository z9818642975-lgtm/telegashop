from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from bot.constants.callbacks import CB
from bot.keyboards.inline.admin_panel import admin_panel_kb
from bot.models.operator_salary import OperatorSalary
from bot.models.operator_shift import OperatorShift

router = Router(name="admin_panel")

@router.callback_query(F.data == CB.ADMIN_PANEL)
async def admin_panel(cb: CallbackQuery):
    await cb.message.edit_text(
        "рџ‘‘ <b>РђРґРјРёРЅ-РїР°РЅРµР»СЊ</b>",
        reply_markup=admin_panel_kb(),
    )
    await cb.answer()

@router.callback_query(F.data == CB.ADMIN_SALARY)
async def admin_salary(cb: CallbackQuery, *, session: AsyncSession | None = None):
    result = await session.execute(
        select(
            OperatorSalary.operator_id,
            func.sum(OperatorSalary.amount)
        ).group_by(OperatorSalary.operator_id)
    )
    rows = result.all()

    text = "рџ’° <b>Р—Р°СЂРїР»Р°С‚Р° РѕРїРµСЂР°С‚РѕСЂРѕРІ</b>\n\n"
    if not rows:
        text += "РќРµС‚ РґР°РЅРЅС‹С…"
    else:
        for operator_id, total in rows:
            text += f"рџ‘· {operator_id}: {total} в‚Ѕ\n"

    await cb.message.edit_text(text, reply_markup=admin_panel_kb())
    await cb.answer()

@router.callback_query(F.data == CB.ADMIN_SLA)
async def admin_sla(cb: CallbackQuery, *, session: AsyncSession | None = None):
    result = await session.execute(
        select(OperatorShift).where(OperatorShift.closed_at.is_(None))
    )
    shifts = result.scalars().all()

    text = "вЏ± <b>SLA РѕРїРµСЂР°С‚РѕСЂРѕРІ</b>\n\n"
    if not shifts:
        text += "РђРєС‚РёРІРЅС‹С… СЃРјРµРЅ РЅРµС‚"
    else:
        for s in shifts:
            text += (
                f"рџ‘· {s.operator_id}\n"
                f"рџ•’ РќР°С‡Р°Р»Рѕ: {s.started_at}\n\n"
            )

    await cb.message.edit_text(text, reply_markup=admin_panel_kb())
    await cb.answer()


