$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1) КНОПКИ ЧАТА И ЭСКАЛАЦИИ
# ======================================================
MkFile "$base/keyboards/chat.py" @'
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def chat_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💬 Написать сообщение",
                callback_data=f"chat:msg:{order_id}"
            ),
            InlineKeyboardButton(
                text="👑 Позвать админа",
                callback_data=f"chat:escalate:{order_id}"
            ),
        ]
    ])
'@

MkFile "$base/routers/chat.py" @'
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.services.chat_antispam import check_client_rate_limit
from bot_refactored.services.admin_chat_alert import notify_admin_chat_request
from bot_refactored.constants.roles import ADMINS

router = Router(name="chat")

@router.callback_query(F.data.startswith("chat:escalate:"))
async def escalate(cb: CallbackQuery):
    order_id = int(cb.data.split(":")[-1])
    for admin_id in ADMINS:
        await notify_admin_chat_request(
            cb.bot, admin_id, order_id, cb.from_user.id
        )
    await cb.answer("Администратор уведомлён")

@router.message(F.text)
async def chat_message(msg: Message, session: AsyncSession):
    # анти-спам для клиента
    if not check_client_rate_limit(msg.from_user.id):
        await msg.answer("⏱ Можно писать не чаще 1 сообщения в 10 секунд")
        return

    # здесь сохраняется сообщение в OrderChatMessage (у тебя уже есть модель)
    # и пересылается адресату (оператору/клиенту)
    await msg.answer("Сообщение отправлено")
'@

# ======================================================
# 2) АДМИН: СОЗДАНИЕ И АРХИВАЦИЯ ОПЕРАТОРОВ
# ======================================================
MkFile "$base/models/operator.py" @'
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean
from bot_refactored.db import Base

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
'@

MkFile "$base/dao/operators.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.operator import Operator

class OperatorsDAO:
    @staticmethod
    async def create(session: AsyncSession, telegram_id: int):
        op = Operator(telegram_id=telegram_id, is_active=True)
        session.add(op)
        return op

    @staticmethod
    async def archive(session: AsyncSession, telegram_id: int):
        res = await session.execute(
            select(Operator).where(Operator.telegram_id == telegram_id)
        )
        op = res.scalar_one_or_none()
        if not op:
            raise ValueError("operator not found")
        op.is_active = False
        return op

    @staticmethod
    async def list_all(session: AsyncSession):
        res = await session.execute(select(Operator))
        return res.scalars().all()
'@

MkFile "$base/app/admin/operators.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operators import OperatorsDAO

class CreateOperatorUseCase:
    def __init__(self, telegram_id: int, session: AsyncSession):
        self.telegram_id = telegram_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            await OperatorsDAO.create(self.session, self.telegram_id)

class ArchiveOperatorUseCase:
    def __init__(self, telegram_id: int, session: AsyncSession):
        self.telegram_id = telegram_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            await OperatorsDAO.archive(self.session, self.telegram_id)
'@

MkFile "$base/routers/admin/operators.py" @'
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.constants.roles import ADMINS
from bot_refactored.app.admin.operators import (
    CreateOperatorUseCase,
    ArchiveOperatorUseCase,
)

router = Router(name="admin_operators")

def _is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.message(F.text.startswith("/add_operator"))
async def add_operator(msg: Message, session: AsyncSession):
    if not _is_admin(msg.from_user.id):
        return
    telegram_id = int(msg.text.split()[-1])
    await CreateOperatorUseCase(telegram_id, session).execute()
    await msg.answer("Оператор добавлен")

@router.message(F.text.startswith("/archive_operator"))
async def archive_operator(msg: Message, session: AsyncSession):
    if not _is_admin(msg.from_user.id):
        return
    telegram_id = int(msg.text.split()[-1])
    await ArchiveOperatorUseCase(telegram_id, session).execute()
    await msg.answer("Оператор архивирован")
'@

Write-Host "Chat buttons + escalation + admin operator CRUD added." -ForegroundColor Green
