from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.products_dao import ProductsDAO
from bot.keyboards.client.catalog import catalog_kb
from bot.models.user import User


async def show_catalog(
    *,
    message: Message,
    session: AsyncSession,
    user: User,
) -> None:
    products = await ProductsDAO.get_active(session)

    if not products:
        await message.edit_text(
            "рџ“¦ РљР°С‚Р°Р»РѕРі РїСѓСЃС‚",
            reply_markup=None,
        )
        return

    await message.edit_text(
        "рџ“¦ <b>РљР°С‚Р°Р»РѕРі</b>\n\nР’С‹Р±РµСЂРёС‚Рµ С‚РѕРІР°СЂ:",
        reply_markup=catalog_kb(products),
    )

