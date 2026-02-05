# bot/routers/admin/stocks.py
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_admin import AdminWarehouseProductsCB
from bot.dao.products_dao import ProductsDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.filters.role import RoleFilter
from bot.utils.safe_edit import safe_edit_text

router = Router(name="admin_stocks")


# ============================================================
# 📦 ОСТАТКИ ПО СКЛАДУ
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminWarehouseProductsCB.filter())
async def warehouse_stocks(
    cb: CallbackQuery,
    callback_data: AdminWarehouseProductsCB,
    session: AsyncSession,
):
    wh_dao = WarehousesDAO(session)
    prod_dao = ProductsDAO(session)

    warehouse = await wh_dao.get_by_id(callback_data.warehouse_id)
    if not warehouse:
        await cb.answer("Склад не найден", show_alert=True)
        return

    rows = await prod_dao.list_with_stock(warehouse_id=warehouse.id)

    text = f"📦 <b>Остатки склада</b>\n🏬 {warehouse.title}\n\n"

    if not rows:
        text += "Нет товаров"
    else:
        for r in rows:
            text += (
                f"{r.title}\n"
                f"  Остаток: <b>{r.qty_available}</b>\n\n"
            )

    await safe_edit_text(
        cb.message,
        text=text,
        parse_mode="HTML",
        reply_markup=None,
    )
    await cb.answer()

