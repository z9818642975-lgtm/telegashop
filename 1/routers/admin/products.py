from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.products_dao import ProductsDAO
from bot.keyboards.admin.products import products_kb

router = Router(name="admin_products")

@router.callback_query(RoleFilter("admin"), F.data == "admin:products")
async def products_list(cb, *, session: AsyncSession | None = None):
    dao = ProductsDAO(session)
    products = await dao.list_all()
    await cb.message.edit_text("Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ Р В Р’В Р РЋРЎвЂєР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“", reply_markup=products_kb(products))
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:product:toggle"))
async def product_toggle(cb, *, session: AsyncSession | None = None):
    product_id = int(cb.data.split(":")[-1])
    dao = ProductsDAO(session)
    await dao.toggle_active(product_id)
    await session.commit()
    products = await dao.list_all()
    await cb.message.edit_reply_markup(reply_markup=products_kb(products))
    await cb.answer("OK")



