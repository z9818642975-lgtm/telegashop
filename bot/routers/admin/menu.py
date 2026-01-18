from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.filters.role import RoleFilter
from bot.keyboards.admin.panel import admin_panel_kb

router = Router(name="admin_menu")


@router.callback_query(RoleFilter("admin"), F.data == "admin:panel")
async def admin_panel(cb: CallbackQuery):
    await cb.message.edit_text(
        "🛠 <b>Админ-панель</b>",
        reply_markup=admin_panel_kb(),
    )
    await cb.answer()

