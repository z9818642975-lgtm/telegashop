$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1. INLINE-КЛАВИАТУРЫ АДМИНА
# ======================================================
MkFile "$base/keyboards/admin.py" @'
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👷 Операторы", callback_data="admin:operators")],
        [InlineKeyboardButton(text="💬 Чаты", callback_data="admin:chats")],
    ])

def operators_kb(operators, page: int, pages: int):
    kb = []
    for op in operators:
        kb.append([
            InlineKeyboardButton(
                text=f"👷 {op.telegram_id} ({'ON' if op.is_active else 'OFF'})",
                callback_data=f"admin:operator:{op.telegram_id}"
            )
        ])
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"admin:operators:{page-1}"))
    if page < pages:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"admin:operators:{page+1}"))
    if nav:
        kb.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=kb)
'@

# ======================================================
# 2. АДМИН РОУТЕР С ПАГИНАЦИЕЙ
# ======================================================
MkFile "$base/routers/admin/panel.py" @'
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.keyboards.admin import admin_main_kb, operators_kb
from bot_refactored.dao.operators import OperatorsDAO
from bot_refactored.constants.roles import ADMINS

router = Router(name="admin_panel")

PAGE_SIZE = 5

def _is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.callback_query(F.data == "admin:panel")
async def admin_panel(cb: CallbackQuery):
    if not _is_admin(cb.from_user.id):
        return
    await cb.message.edit_text("👑 Админ-панель", reply_markup=admin_main_kb())

@router.callback_query(F.data.startswith("admin:operators"))
async def operators(cb: CallbackQuery, session: AsyncSession):
    if not _is_admin(cb.from_user.id):
        return

    page = int(cb.data.split(":")[2]) if ":" in cb.data else 1
    ops = await OperatorsDAO.list_all(session)

    total = len(ops)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    await cb.message.edit_text(
        "👷 Операторы:",
        reply_markup=operators_kb(ops[start:end], page, pages)
    )
'@

# ======================================================
# 3. ИСТОРИЯ ЧАТОВ В АДМИНКЕ
# ======================================================
MkFile "$base/routers/admin/chats.py" @'
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.order_chat import OrderChatMessage
from bot_refactored.constants.roles import ADMINS

router = Router(name="admin_chats")

def _is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.callback_query(F.data == "admin:chats")
async def chats(cb: CallbackQuery, session: AsyncSession):
    if not _is_admin(cb.from_user.id):
        return

    res = await session.execute(
        select(OrderChatMessage)
        .order_by(OrderChatMessage.created_at.desc())
        .limit(20)
    )
    messages = res.scalars().all()

    text = ["💬 Последние сообщения:"]
    for m in messages:
        text.append(
            f"[{m.created_at}] #{m.order_id} | {m.sender_id}: {m.text}"
        )

    await cb.message.edit_text("\n".join(text))
'@

Write-Host "Admin inline panel + operator pagination + chat history added." -ForegroundColor Green
