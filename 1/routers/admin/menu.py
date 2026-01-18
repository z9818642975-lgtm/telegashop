from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.filters.role import RoleFilter
from bot.keyboards.admin.panel import admin_panel_kb

router = Router(name="admin_menu")


@router.callback_query(RoleFilter("admin"), F.data == "admin:panel")
async def admin_panel(cb: CallbackQuery):
    await cb.message.edit_text(
        "Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎвЂќР вЂ™Р’В  <b>Р В Р’В Р РЋРІР‚в„ўР В Р’В Р СћРІР‚ВР В Р’В Р РЋР’ВР В Р’В Р РЋРІР‚ВР В Р’В Р В РІР‚В¦-Р В Р’В Р РЋРІР‚вЂќР В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’ВµР В Р’В Р вЂ™Р’В»Р В Р Р‹Р В Р вЂ°</b>",
        reply_markup=admin_panel_kb(),
    )
    await cb.answer()

