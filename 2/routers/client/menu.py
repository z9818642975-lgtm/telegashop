from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.client.main import client_main_menu
from bot.models.user import User

router = Router(name="client_menu")


# ============================
# MAIN MENU
# ============================

@router.message(F.text.in_({"/start", "🏠 Меню"}))
async def show_menu(
    message: Message,
    user: User,
):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=client_main_menu(),
    )


# ============================
# CATALOG
# ============================

@router.message(F.text == "📦 Каталог")
async def catalog_redirect(message: Message):
    """
    Каталог обрабатывается в client/catalog.py.
    Здесь ничего не делаем, чтобы не было дублей.
    """
    # Ничего не отправляем намеренно
    return


# ============================
# PICKUP INFO
# ============================

@router.message(F.text == "📍 Адрес самовывоза")
async def pickup_info(
    message: Message,
    user: User,
):
    await message.answer(
        "📍 Адрес самовывоза отображается при оформлении заказа.",
        reply_markup=client_main_menu(),
    )


# ============================
# PROFILE
# ============================

@router.message(F.text == "👤 Профиль")
async def profile(
    message: Message,
    session: AsyncSession,
    user: User,
):
    await message.answer(
        "👤 <b>Профиль</b>\n\n"
        f"ID: {user.id}\n"
        f"Роль: {user.role}",
        reply_markup=client_main_menu(),
    )


# ============================
# FAQ
# ============================

@router.message(F.text == "❓ FAQ")
async def faq(
    message: Message,
    user: User,
):
    await message.answer(
        "❓ <b>FAQ</b>\n\n"
        "1️⃣ Откройте каталог\n"
        "2️⃣ Выберите товар\n"
        "3️⃣ Добавьте в корзину\n"
        "4️⃣ Оформите заказ\n"
        "5️⃣ Загрузите чек",
        reply_markup=client_main_menu(),
    )


# ============================
# SUPPORT
# ============================

@router.message(F.text == "💬 Связь с оператором")
async def support(
    message: Message,
    user: User,
):
    await message.answer(
        "💬 Оператор подключается автоматически после оплаты заказа.",
        reply_markup=client_main_menu(),
    )

