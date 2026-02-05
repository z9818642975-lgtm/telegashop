# bot/routers/admin/warehouses.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import AdminWarehouseSelectCB, AdminWarehousesListCB
from bot.dao.warehouses_dao import WarehousesDAO
from bot.filters.role import RoleFilter
from bot.keyboards.admin.warehouse_actions import warehouse_actions_kb
from bot.keyboards.admin.warehouses import warehouses_kb
from bot.utils.safe_edit import safe_edit_text

router = Router(name="admin_warehouses")


@router.callback_query(RoleFilter("admin"), AdminWarehousesListCB.filter())
async def warehouses_list(cb: CallbackQuery, session: AsyncSession):
    dao = WarehousesDAO(session)
    warehouses = await dao.list_active()

    await safe_edit_text(
        cb.message,
        text="А 🏬 <b>Склады</b>",
        reply_markup=warehouses_kb(warehouses),
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(RoleFilter("admin"), AdminWarehouseSelectCB.filter())
async def warehouse_card(
    cb: CallbackQuery,
    callback_data: AdminWarehouseSelectCB,
):
    await safe_edit_text(
        cb.message,
        text=f"🏬 <b>Склад #{callback_data.warehouse_id}</b>",
        reply_markup=warehouse_actions_kb(callback_data.warehouse_id),
        parse_mode="HTML",
    )
    await cb.answer()