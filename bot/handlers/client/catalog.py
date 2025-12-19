from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.db import get_session
from bot.dao.products_dao import ProductsDAO

router = Router()

@router.message(F.text == "📦 Каталог")
async def catalog(m: Message, session: AsyncSession = get_session()):
    products = await ProductsDAO(session).list_active()
    if not products:
        await m.answer("Каталог пуст (добавь товары в БД).")
        return
    txt = "Каталог:\n" + "\n".join([f"{p.id}. {p.title}" for p in products])
    await m.answer(txt + "\n\n(UX-кнопки/корзина подключаются, каркас готов)")
