# bot/routers/client/catalog.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_client import CatalogOpen, ProductOpen
from bot.dao.orders_dao import OrdersDAO
from bot.dao.products_dao import ProductsDAO
from bot.keyboards.client.catalog import client_catalog_kb
from bot.keyboards.client.quantity import client_quantity_kb

router = Router(name="client_catalog")


@router.callback_query(CatalogOpen.filter())
async def catalog_open(cb: CallbackQuery, session: AsyncSession):
    products = await ProductsDAO(session).list_active()

    await cb.message.edit_text(
        "📚 Каталог товаров",
        reply_markup=client_catalog_kb(products),
    )
    await cb.answer()


@router.callback_query(ProductOpen.filter())
async def product_open(
    cb: CallbackQuery,
    callback_data: ProductOpen,
    session: AsyncSession,
):
    """
    Клиент выбрал товар → показываем выбор количества
    """
    # гарантируем, что корзина существует
    await OrdersDAO(session).get_or_create_cart(
        user_id=cb.from_user.id
    )

    await cb.message.edit_text(
        "🔢 Выберите количество",
        reply_markup=client_quantity_kb(
            item_id=callback_data.product_id
        ),
    )
    await cb.answer()
