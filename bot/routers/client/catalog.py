from __future__ import annotations

from typing import Union

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.products_dao import ProductsDAO
from bot.dao.orders_dao import OrdersDAO
from bot.keyboards.client.catalog import catalog_kb
from bot.keyboards.client.quantity import quantity_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="client_catalog")


# ============================
# OPEN CATALOG
# ============================

@router.callback_query(F.data == CB.CATALOG_OPEN)
async def open_catalog(cb: CallbackQuery, session: AsyncSession):
    await render_catalog(cb, session)


async def render_catalog(
    event: Union[CallbackQuery, Message],
    session: AsyncSession,
):
    products = await ProductsDAO(session).get_active()

    text = "📦 <b>Каталог</b>\n\nВыберите товар:"

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text,
            reply_markup=catalog_kb(products),
        )
    else:
        await event.answer(
            text,
            reply_markup=catalog_kb(products),
        )


# ============================
# OPEN PRODUCT CARD
# ============================

@router.callback_query(F.data.startswith("product:"))

async def open_product(cb: CallbackQuery, session: AsyncSession):
    product_id = int(cb.data.split(":")[2])

    product = await ProductsDAO(session).get_by_id(product_id)
    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Добавить в корзину",
                    callback_data=f"product:add:{product.id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=CB.CATALOG_OPEN,
                )
            ],
        ]
    )

    await cb.message.edit_text(
        (
            f"📦 <b>{product.title}</b>\n\n"
            f"Цена: <b>{product.base_price} ₽</b>"
        ),
        reply_markup=kb,
    )


# ============================
# ADD PRODUCT → CREATE ORDER ITEM
# ============================

@router.callback_query(F.data.startswith("product:add:"))
async def add_product(cb: CallbackQuery, session: AsyncSession, user):
    product_id = int(cb.data.split(":")[2])

    orders = OrdersDAO(session)
    item = await orders.add_product(
        user_id=user.id,
        product_id=product_id,
        qty=1,  # стартовое значение
    )

    await cb.message.edit_text(
        "Выберите количество:",
        reply_markup=quantity_kb(item.id),
    )
