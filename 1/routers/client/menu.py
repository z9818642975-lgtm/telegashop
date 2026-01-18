from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.client.main import client_main_menu
from bot.models.user import User

router = Router(name="client_menu")


# ❌ DISABLED (text-based handler)
async def show_menu(
    message: Message,
    *,
    user: User | None = None,
):
    await message.answer(
        "рџЏ  <b>Р“Р»Р°РІРЅРѕРµ РјРµРЅСЋ</b>",
        reply_markup=client_main_menu(),
    )


# ❌ DISABLED (text-based handler)
async def catalog_redirect(message: Message):
    # РљР°С‚Р°Р»РѕРі РѕР±СЂР°Р±Р°С‚С‹РІР°РµС‚СЃСЏ РІ client/catalog.py
    return


# ❌ DISABLED (text-based handler)
async def pickup_info(
    message: Message,
    *,
    user: User | None = None,
):
    await message.answer(
        "рџ“Ќ РђРґСЂРµСЃ СЃР°РјРѕРІС‹РІРѕР·Р° РѕС‚РѕР±СЂР°Р¶Р°РµС‚СЃСЏ РїСЂРё РѕС„РѕСЂРјР»РµРЅРёРё Р·Р°РєР°Р·Р°.",
        reply_markup=client_main_menu(),
    )


# ❌ DISABLED (text-based handler)
async def profile(
    message: Message,
    *,
    session: AsyncSession | None = None,
    user: User | None = None,
):
    await message.answer(
        "рџ‘¤ <b>РџСЂРѕС„РёР»СЊ</b>\n\n"
        f"ID: {user.id if user else 'вЂ”'}\n"
        f"Р РѕР»СЊ: {user.role if user else 'вЂ”'}",
        reply_markup=client_main_menu(),
    )


# ❌ DISABLED (text-based handler)
async def faq(
    message: Message,
    *,
    user: User | None = None,
):
    await message.answer(
        "вќ“ <b>FAQ</b>\n\n"
        "1пёЏвѓЈ РћС‚РєСЂРѕР№С‚Рµ РєР°С‚Р°Р»РѕРі\n"
        "2пёЏвѓЈ Р’С‹Р±РµСЂРёС‚Рµ С‚РѕРІР°СЂ\n"
        "3пёЏвѓЈ Р”РѕР±Р°РІСЊС‚Рµ РІ РєРѕСЂР·РёРЅСѓ\n"
        "4пёЏвѓЈ РћС„РѕСЂРјРёС‚Рµ Р·Р°РєР°Р·\n"
        "5пёЏвѓЈ Р—Р°РіСЂСѓР·РёС‚Рµ С‡РµРє",
        reply_markup=client_main_menu(),
    )


# ❌ DISABLED (text-based handler)
async def support(
    message: Message,
    *,
    user: User | None = None,
):
    await message.answer(
        "рџ’¬ РћРїРµСЂР°С‚РѕСЂ РїРѕРґРєР»СЋС‡Р°РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РїРѕСЃР»Рµ РѕРїР»Р°С‚С‹ Р·Р°РєР°Р·Р°.",
        reply_markup=client_main_menu(),
    )

