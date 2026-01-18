from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.warehouses_dao import WarehousesDAO
from bot.keyboards.admin.warehouses import warehouses_kb
from bot.keyboards.admin.warehouse_actions import warehouse_actions_kb

router = Router(name="admin_warehouses")


@router.callback_query(RoleFilter("admin"), F.data == "admin:warehouses")
async def warehouses_list(cb, *, session: AsyncSession | None = None):
    dao = WarehousesDAO(session)
    warehouses = await dao.list_all()

    await cb.message.edit_text(
        "Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ <b>Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚ВР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“</b>",
        reply_markup=warehouses_kb(warehouses),
    )
    await cb.answer()


@router.callback_query(
    RoleFilter("admin"),
    F.data.startswith("admin:wh:")
    & ~F.data.contains(":products")
    & ~F.data.contains(":move"),
)
async def warehouse_card(cb: CallbackQuery):
    warehouse_id = int(cb.data.split(":")[-1])

    await cb.message.edit_text(
        f"Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ <b>Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В #{warehouse_id}</b>",
        reply_markup=warehouse_actions_kb(warehouse_id),
    )
    await cb.answer()



