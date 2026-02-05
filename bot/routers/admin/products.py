# bot/routers/admin/products.py
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_admin import AdminProductCard, AdminProducts, AdminProductToggle
from bot.dao.products_dao import ProductsDAO
from bot.filters.role import RoleFilter
from bot.keyboards.admin.main import admin_main_menu_kb
from bot.keyboards.admin.products import admin_products_kb

router = Router(name="admin_products")

# ============================================================
# 📦 СПИСОК ТОВАРОВ
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminProducts.filter())
async def admin_products_list(
    cb: CallbackQuery,
    session: AsyncSession,
):
    dao = ProductsDAO(session)
    products = await dao.list_all()

    await cb.message.edit_text(
        "📦 <b>Товары</b>\n\nВыберите товар:",
        reply_markup=admin_products_kb(products),
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# 📦 КАРТОЧКА ТОВАРА
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminProductCard.filter())
async def admin_product_card(
    cb: CallbackQuery,
    callback_data: AdminProductCard,
    session: AsyncSession,
):
    dao = ProductsDAO(session)
    product = await dao.get(callback_data.product_id)

    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    text = (
        f"📦 <b>{product.title}</b>\n\n"
        f"💰 Цена: {product.price}\n"
        f"📦 Остаток: {product.stock}\n"
        f"🟢 Активен: {'да' if product.is_active else 'нет'}"
    )

    await cb.message.edit_text(
        text,
        reply_markup=admin_products_kb([product], single=True),
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# 🔁 АКТИВАЦИЯ / ДЕАКТИВАЦИЯ
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminProductToggle.filter())
async def admin_product_toggle(
    cb: CallbackQuery,
    callback_data: AdminProductToggle,
    session: AsyncSession,
):
    dao = ProductsDAO(session)
    await dao.toggle_active(callback_data.product_id)
    await session.commit()

    await cb.answer("Статус изменён")
    # возвращаемся к списку
    await admin_products_list(cb, session)


# ============================================================
# ⬅️ BACK В АДМИН-МЕНЮ
# ============================================================

@router.callback_query(RoleFilter("admin"))
async def admin_products_back(cb: CallbackQuery):
    await cb.message.edit_text(
        "👑 <b>Админ-панель</b>\nВыберите раздел:",
        reply_markup=admin_main_menu_kb(),
        parse_mode="HTML",
    )
    await cb.answer()

