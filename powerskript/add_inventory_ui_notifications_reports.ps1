$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1. TELEGRAM УВЕДОМЛЕНИЯ (SLA)
# ======================================================
MkFile "$base/services/notifications.py" @'
from aiogram import Bot

async def notify(bot: Bot, user_id: int, text: str):
    await bot.send_message(user_id, text)
'@

MkFile "$base/services/operator_sla_notifier.py" @'
from datetime import timedelta
from bot_refactored.services.notifications import notify

async def process_shift_sla(bot, shift, delta):
    if delta >= timedelta(minutes=15):
        await notify(bot, shift.operator_id, "⚠️ Вы неактивны 15 минут")
    if delta >= timedelta(minutes=17):
        await notify(bot, shift.operator_id, "⚠️ Вы неактивны 17 минут")
    if delta >= timedelta(minutes=18):
        await notify(bot, shift.operator_id, "❗ Вы неактивны 18 минут")
    if delta >= timedelta(minutes=20):
        await notify(bot, shift.operator_id, "⛔ Смена закрыта автоматически")
'@

# ======================================================
# 2. UI КАРТОЧКИ ОСТАТКОВ
# ======================================================
MkFile "$base/services/inventory_ui.py" @'
from bot_refactored.models.inventory import InventoryItem

def render_operator_inventory(items: list[InventoryItem]) -> str:
    lines = ["📦 Ваши остатки:"]
    for i in items:
        free = i.quantity - i.reserved
        lines.append(
            f"Товар {i.product_id}: свободно {free}, резерв {i.reserved}"
        )
    return "\n".join(lines)

def render_admin_inventory(items: list[InventoryItem]) -> str:
    lines = ["📦 Остатки по операторам:"]
    for i in items:
        lines.append(
            f"Оператор {i.operator_id}, товар {i.product_id}: "
            f"{i.quantity} (резерв {i.reserved})"
        )
    return "\n".join(lines)
'@

# ======================================================
# 3. DAO ДЛЯ ОТЧЁТА ПО СПИСАНИЯМ
# ======================================================
MkFile "$base/models/inventory_log.py" @'
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base

class InventoryLog(Base):
    __tablename__ = "inventory_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int]
    qty: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
'@

MkFile "$base/dao/inventory_log.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.inventory_log import InventoryLog

class InventoryLogDAO:
    @staticmethod
    async def write(session: AsyncSession, operator_id: int, product_id: int, qty: int):
        session.add(
            InventoryLog(
                operator_id=operator_id,
                product_id=product_id,
                qty=qty,
            )
        )

    @staticmethod
    async def report(session: AsyncSession):
        res = await session.execute(select(InventoryLog))
        return res.scalars().all()
'@

# ======================================================
# 4. ОТЧЁТ ПО СПИСАНИЯМ (UI)
# ======================================================
MkFile "$base/services/inventory_report.py" @'
from bot_refactored.models.inventory_log import InventoryLog

def render_inventory_report(logs: list[InventoryLog]) -> str:
    lines = ["📊 Отчёт по списаниям:"]
    for l in logs:
        lines.append(
            f"{l.created_at} | Оператор {l.operator_id} | "
            f"Товар {l.product_id} | -{l.qty}"
        )
    return "\n".join(lines)
'@

Write-Host "Inventory UI + notifications + reports added." -ForegroundColor Green
