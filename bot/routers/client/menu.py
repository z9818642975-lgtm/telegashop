# bot/routers/client/menu.py
from aiogram import F, Router
from aiogram.types import Message

router = Router(name="client_menu")


# ⬅️ ТОЛЬКО ЯВНЫЙ ВХОД В МЕНЮ
@router.message(F.text == "📦 Каталог")
async def client_catalog(msg: Message):
    await msg.answer("📚 Каталог")


@router.message(F.text == "🛒 Корзина")
async def client_cart(msg: Message):
    await msg.answer("🛒 Корзина")


@router.message(F.text == "👤 Профиль")
async def client_profile(msg: Message):
    await msg.answer("👤 Профиль")


@router.message(F.text == "❓ FAQ")
async def client_faq(msg: Message):
    await msg.answer("❓ FAQ")


@router.message(F.text == "💬 Связь с оператором")
async def client_support(msg: Message):
    await msg.answer("💬 Связь с оператором")


# ⛔️ УДАЛИТЬ ПОЛНОСТЬЮ
# @router.message()
# async def client_menu(...)
