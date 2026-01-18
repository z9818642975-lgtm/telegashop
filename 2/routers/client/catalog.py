# bot/routers/client/catalog.py
from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.products_dao import ProductsDAO
from bot.keyboards.client.catalog import catalog_kb
from bot.keyboards.client.quantity import quantity_kb

router = Router(name="client_catalog")


# ============================
# OPEN CATALOG
# ============================

@router.callback_query(F.data == CB.CATALOG)
async def open_catalog(cb: CallbackQuery, session: AsyncSession):
    await render_catalog(cb, session)


async def render_catalog(cb: CallbackQuery, session: AsyncSession):
    products = await ProductsDAO(session).get_active()

    await cb.message.edit_text(
        "📦 <b>Каталог</b>\n\nВыберите товар:",
        reply_markup=catalog_kb(products),
    )


# ============================
# OPEN PRODUCT → QTY
# ============================

@router.callback_query(F.data.startswith("product:"))
async def open_product(cb: CallbackQuery, session: AsyncSession):
    product_id = int(cb.data.split(":")[1])

    product = await ProductsDAO(session).get_by_id(product_id)
    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    await cb.message.edit_text(
        (
            f"📦 <b>{product.title}</b>\n\n"
            f"Цена: <b>{product.base_price} ₽</b>\n\n"
            f"Выберите количество:"
        ),
        reply_markup=quantity_kb(product.id),
    )


# ============================
# BACK TO CATALOG
# ============================

@router.callback_query(F.data == CB.BACK_CATALOG)
async def back_to_catalog(cb: CallbackQuery, session: AsyncSession):
    await render_catalog(cb, session)

