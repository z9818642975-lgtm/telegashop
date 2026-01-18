$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1. ЦЕНТРАЛЬНЫЙ СКЛАД
# ======================================================
MkFile "$base/models/central_inventory.py" @'
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base

class CentralInventory(Base):
    __tablename__ = "central_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(default=0)
'@

MkFile "$base/dao/central_inventory.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_refactored.models.central_inventory import CentralInventory

class CentralInventoryDAO:
    @staticmethod
    async def get_for_update(session: AsyncSession, product_id: int):
        res = await session.execute(
            select(CentralInventory)
            .where(CentralInventory.product_id == product_id)
            .with_for_update()
        )
        return res.scalar_one_or_none()
'@

MkFile "$base/app/inventory/transfer_to_operator.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.central_inventory import CentralInventoryDAO
from bot_refactored.dao.inventory import InventoryDAO

class TransferToOperatorUseCase:
    def __init__(
        self,
        *,
        product_id: int,
        qty: int,
        operator_id: int,
        session: AsyncSession,
    ):
        self.product_id = product_id
        self.qty = qty
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            central = await CentralInventoryDAO.get_for_update(
                self.session, self.product_id
            )
            if not central or central.quantity < self.qty:
                raise ValueError("not enough central stock")

            central.quantity -= self.qty

            item = await InventoryDAO.get_for_update(
                self.session,
                operator_id=self.operator_id,
                product_id=self.product_id,
            )
            if not item:
                raise ValueError("operator inventory not found")

            item.quantity += self.qty
'@

# ======================================================
# 2. МИНИМАЛЬНЫЕ ОСТАТКИ + АЛЕРТЫ
# ======================================================
MkFile "$base/models/inventory_limits.py" @'
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base

class InventoryLimit(Base):
    __tablename__ = "inventory_limits"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    min_qty: Mapped[int] = mapped_column(default=0)
'@

MkFile "$base/services/inventory_alerts.py" @'
from bot_refactored.models.inventory import InventoryItem
from bot_refactored.models.inventory_limits import InventoryLimit

def check_min_limit(item: InventoryItem, limit: InventoryLimit | None) -> bool:
    if not limit:
        return False
    return (item.quantity - item.reserved) <= limit.min_qty
'@

# ======================================================
# 3. УВЕДОМЛЕНИЯ КЛИЕНТУ О СТАТУСАХ
# ======================================================
MkFile "$base/services/client_notifications.py" @'
from aiogram import Bot

async def notify_client(bot: Bot, client_id: int, text: str):
    await bot.send_message(client_id, text)
'@

# ======================================================
# 4. ЧАТ КЛИЕНТ–ОПЕРАТОР + ПОЗВАТЬ АДМИНА
# ======================================================
MkFile "$base/models/order_chat.py" @'
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from bot_refactored.db import Base

class OrderChatMessage(Base):
    __tablename__ = "order_chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    sender_id: Mapped[int]
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
'@

MkFile "$base/services/admin_chat_alert.py" @'
from aiogram import Bot

async def notify_admin_chat_request(
    bot: Bot,
    admin_id: int,
    order_id: int,
    from_user: int,
):
    await bot.send_message(
        admin_id,
        f"👑 Запрос администратора\nЗаказ #{order_id}\nПользователь {from_user}"
    )
'@

# ======================================================
# 5. УВЕДОМЛЕНИЕ АДМИНУ О КАЖДОЙ ОПЛАТЕ
# ======================================================
MkFile "$base/services/admin_payment_notify.py" @'
from aiogram import Bot

async def notify_admin_payment(
    bot: Bot,
    admin_id: int,
    order_id: int,
    operator_id: int,
):
    await bot.send_message(
        admin_id,
        f"💰 Заказ #{order_id} оплачен\nОператор {operator_id}"
    )
'@

Write-Host "Central stock, alerts, client notifications, chat & admin notifications added." -ForegroundColor Green
