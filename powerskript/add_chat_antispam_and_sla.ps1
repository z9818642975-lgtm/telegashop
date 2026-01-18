$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1. РОЛИ (ОДИН АДМИН, СПИСОК ОПЕРАТОРОВ)
# ======================================================
MkFile "$base/constants/roles.py" @'
ADMINS = {7444294101}
OPERATORS = {8413852743}
'@

# ======================================================
# 2. АНТИ-СПАМ В ЧАТАХ (CLIENT)
# ======================================================
MkFile "$base/services/chat_antispam.py" @'
import time

# user_id -> last_message_ts
_LAST_MESSAGE = {}

RATE_LIMIT_SECONDS = 10  # 1 сообщение / 10 сек


def check_client_rate_limit(user_id: int) -> bool:
    now = time.time()
    last = _LAST_MESSAGE.get(user_id)

    if last and now - last < RATE_LIMIT_SECONDS:
        return False

    _LAST_MESSAGE[user_id] = now
    return True
'@

# ======================================================
# 3. SLA ЧАТА (ОЖИДАНИЕ ОТВЕТА)
# ======================================================
MkFile "$base/models/chat_sla.py" @'
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base


class ChatSLA(Base):
    __tablename__ = "chat_sla"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)

    last_client_msg_at: Mapped[datetime | None]
    last_operator_msg_at: Mapped[datetime | None]
    last_admin_msg_at: Mapped[datetime | None]
'@

# ======================================================
# 4. SLA ПРОЦЕССОР
# ======================================================
MkFile "$base/services/chat_sla.py" @'
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.chat_sla import ChatSLA

OPERATOR_SLA = timedelta(minutes=5)
ADMIN_SLA = timedelta(minutes=10)


async def update_client_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_client_msg_at = datetime.utcnow()


async def update_operator_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_operator_msg_at = datetime.utcnow()


async def update_admin_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_admin_msg_at = datetime.utcnow()


async def get_sla_violations(session: AsyncSession):
    now = datetime.utcnow()
    res = await session.execute(select(ChatSLA))
    slas = res.scalars().all()

    violations = []

    for sla in slas:
        if (
            sla.last_client_msg_at
            and (
                not sla.last_operator_msg_at
                or sla.last_operator_msg_at < sla.last_client_msg_at
            )
            and now - sla.last_client_msg_at > OPERATOR_SLA
        ):
            violations.append(("operator", sla.order_id))

        if (
            sla.last_operator_msg_at
            and (
                not sla.last_admin_msg_at
                or sla.last_admin_msg_at < sla.last_operator_msg_at
            )
            and now - sla.last_operator_msg_at > ADMIN_SLA
        ):
            violations.append(("admin", sla.order_id))

    return violations


async def _get_or_create(session: AsyncSession, order_id: int) -> ChatSLA:
    res = await session.execute(
        select(ChatSLA).where(ChatSLA.order_id == order_id)
    )
    sla = res.scalar_one_or_none()
    if sla:
        return sla

    sla = ChatSLA(order_id=order_id)
    session.add(sla)
    return sla
'@

# ======================================================
# 5. УВЕДОМЛЕНИЯ ПО SLA
# ======================================================
MkFile "$base/services/chat_sla_notify.py" @'
from aiogram import Bot
from bot_refactored.constants.roles import ADMINS


async def notify_operator_sla(bot: Bot, operator_id: int, order_id: int):
    await bot.send_message(
        operator_id,
        f"⏱ SLA: нет ответа клиенту по заказу #{order_id}"
    )


async def notify_admin_sla(bot: Bot, order_id: int):
    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"⛔ SLA: оператор не ответил по заказу #{order_id}"
        )
'@

Write-Host "Chat anti-spam + SLA + fixed admin/operator roles added." -ForegroundColor Green
