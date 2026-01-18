from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
import tempfile

from bot.dao.reports import ReportsDAO
from bot.keyboards.inline.reports_panel import reports_panel_kb
from bot.services.export import ExportService
from bot.constants.callbacks_reports import CB_REPORTS

router = Router(name="admin_reports_panel")

@router.callback_query(F.data == CB_REPORTS.REPORTS_MENU)
async def reports_menu(cb: CallbackQuery):
    await cb.message.edit_text(
        "рџ“Љ <b>РћС‚С‡С‘С‚С‹</b>",
        reply_markup=reports_panel_kb(),
    )
    await cb.answer()

@router.callback_query(F.data == CB_REPORTS.REPORTS_BY_OPERATOR)
async def report_by_operator(cb: CallbackQuery, *, session: AsyncSession | None = None):
    orders = await ReportsDAO.orders_by_operator(session)
    salary = await ReportsDAO.salary_by_operator(session)

    text = "рџ‘· <b>РћС‚С‡С‘С‚ РїРѕ РѕРїРµСЂР°С‚РѕСЂР°Рј</b>\n\n"
    for op_id, cnt in orders:
        total = next((s for o, s in salary if o == op_id), 0)
        text += f"рџ‘· {op_id}: Р·Р°РєР°Р·РѕРІ {cnt}, РґРѕС…РѕРґ {total} в‚Ѕ\n"

    await cb.message.edit_text(text, reply_markup=reports_panel_kb())
    await cb.answer()

@router.callback_query(F.data == CB_REPORTS.REPORTS_EXPORT_CSV)
async def export_csv(cb: CallbackQuery, *, session: AsyncSession | None = None):
    orders = await ReportsDAO.all_orders(session)
    csv_data = ExportService.orders_to_csv(orders)

    await cb.message.answer_document(
        document=csv_data.encode("utf-8"),
        filename="orders.csv",
    )
    await cb.answer()

@router.callback_query(F.data == CB_REPORTS.REPORTS_EXPORT_PDF)
async def export_pdf(cb: CallbackQuery, *, session: AsyncSession | None = None):
    orders = await ReportsDAO.all_orders(session)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        ExportService.orders_to_pdf(tmp.name, orders)
        await cb.message.answer_document(
            FSInputFile(tmp.name, filename="orders.pdf")
        )
    await cb.answer()


