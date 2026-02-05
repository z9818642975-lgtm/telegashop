# bot/routers/client/cart.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import (
    ClientCartCheckout,
    ClientCartClear,
    ClientCartOpen,
    ClientItemQty,
    ClientItemRemove,
)
from bot.dao.orders_dao import OrdersDAO
from bot.keyboards.client.cart import client_cart_kb

router = Router(name="client_cart")


@router.callback_query(ClientCartOpen.filter())
async def cart_open(cb: CallbackQuery, session: AsyncSession):
    dao = OrdersDAO(session)
    items = await dao.get_cart_items(user_id=cb.from_user.id)

    await cb.message.edit_text(
        "🛒 Ваша корзина",
        reply_markup=client_cart_kb(items),
    )
    await cb.answer()


@router.callback_query(ClientItemQty.filter())
async def change_qty(
    cb: CallbackQuery,
    callback_data: ClientItemQty,
    session: AsyncSession,
):
    dao = OrdersDAO(session)
    await dao.set_item_qty(
        item_id=callback_data.item_id,
        qty=callback_data.qty,
    )

    await cb.answer("Количество обновлено")


@router.callback_query(ClientItemRemove.filter())
async def remove_item(
    cb: CallbackQuery,
    callback_data: ClientItemRemove,
    session: AsyncSession,
):
    dao = OrdersDAO(session)
    await dao.remove_item(item_id=callback_data.item_id)

    await cb.answer("Товар удалён")


@router.callback_query(ClientCartClear.filter())
async def clear_cart(cb: CallbackQuery, session: AsyncSession):
    dao = OrdersDAO(session)
    await dao.clear_cart(user_id=cb.from_user.id)

    await cb.answer("Корзина очищена")
    await cb.message.edit_text("🧺 Корзина пуста")


@router.callback_query(ClientCartCheckout.filter())
async def checkout(cb: CallbackQuery):
    await cb.message.edit_text("🚚 Выберите способ доставки")
    await cb.answer()