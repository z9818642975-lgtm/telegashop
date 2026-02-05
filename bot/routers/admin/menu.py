from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from bot.constants.callbacks_common import BackCB
from bot.constants.callbacks_admin import (
    AdminBanks,
    AdminOperators,
    AdminOrders,
    AdminProducts,
    AdminSalaryMenuCB,
    AdminWarehousesListCB,
)

from bot.filters.role import RoleFilter
from bot.keyboards.admin.main import admin_main_menu_kb

router = Router(name="admin_menu")

# ============================================================
# ENTRY — REPLY МЕНЮ АДМИНА
# ============================================================

@router.message(RoleFilter("admin"), F.text.in_(["👑 Админ", "🛠 Админ-панель"]))
async def admin_entry(msg: Message):
    await msg.answer(
        "👑 <b>Админ-панель</b>\nВыберите раздел:",
        reply_markup=admin_main_menu_kb(),
        parse_mode="HTML",
    )

# ============================================================
# 📦 ТОВАРЫ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 📦 Товары")
async def admin_products_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 📦 Управление товарами",
                    callback_data=AdminProducts().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "📦 <b>Товары</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminProducts.filter())
async def admin_products_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "📦 <b>Управление товарами</b>\n\n(заглушка)",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# 🏦 БАНКИ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 🏦 Банки")
async def admin_banks_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 🏦 Управление банками",
                    callback_data=AdminBanks().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "🏦 <b>Банки</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminBanks.filter())
async def admin_banks_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "🏦 <b>Банки</b>\n\n(заглушка)",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# 👷 ОПЕРАТОРЫ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 👷 Операторы")
async def admin_operators_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 👷 Список операторов",
                    callback_data=AdminOperators().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "👷 <b>Операторы</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminOperators.filter())
async def admin_operators_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "👷 <b>Операторы</b>\n\n(заглушка)",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# 🏬 СКЛАДЫ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 🏬 Склады")
async def admin_warehouses_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 🏬 Список складов",
                    callback_data=AdminWarehousesListCB().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "🏬 <b>Склады</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminWarehousesListCB.filter())
async def admin_warehouses_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "🏬 <b>Склады</b>\n\n(заглушка)",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# 📋 ЗАКАЗЫ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 📋 Заказы")
async def admin_orders_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 📋 Открыть заказы",
                    callback_data=AdminOrders().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "📋 <b>Заказы</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminOrders.filter())
async def admin_orders_cb(cb: CallbackQuery, callback_data: AdminOrders):
    await cb.message.edit_text(
        f"📋 <b>Заказы</b>\n\nСтраница: {callback_data.page}",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# 💰 ЗАРПЛАТЫ
# ============================================================

@router.message(RoleFilter("admin"), F.text == "А 💰 Зарплаты")
async def admin_salary_menu(msg: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 💰 Зарплаты операторов",
                    callback_data=AdminSalaryMenuCB().pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅️ Назад",
                    callback_data=BackCB().pack(),
                )
            ],
        ]
    )

    await msg.answer(
        "💰 <b>Зарплаты</b>",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(RoleFilter("admin"), AdminSalaryMenuCB.filter())
async def admin_salary_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "💰 <b>Зарплаты</b>\n\n(заглушка)",
        parse_mode="HTML",
    )
    await cb.answer()

# ============================================================
# ⬅️ BACK — СТРОГО ПО CALLBACKDATA
# ============================================================


@router.callback_query(RoleFilter("admin"), BackCB.filter())
async def admin_back_menu(cb: CallbackQuery):
    await cb.message.edit_text(
        "👑 <b>Админ-панель</b>\nВыберите раздел:",
        reply_markup=admin_main_menu_kb(),
        parse_mode="HTML",
    )
    await cb.answer()
