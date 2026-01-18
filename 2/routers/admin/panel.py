from aiogram import Router, F
from aiogram.types import Message

from bot.filters.role import RoleFilter
from bot.keyboards.admin.panel import admin_panel_kb

router = Router(name="admin_panel_entry")

@router.message(RoleFilter("admin"), F.text == "👑 Админ")
async def admin_entry(message: Message):
    await message.answer("👑 Админ-панель", reply_markup=admin_panel_kb())

