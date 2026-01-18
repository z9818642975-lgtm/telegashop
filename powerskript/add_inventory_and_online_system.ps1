$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# =========================================================
# 1. INVENTORY MODEL
# =========================================================
MkFile "$base/models/inventory.py" @'
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from bot_refactored.db import Base


class InventoryItem(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)

    quantity: Mapped[int] = mapped_column(default=0)
    reserved: Mapped[int] = mapped_column(default=0)
'@

# =========================================================
# 2. INVENTORY DAO
# =========================================================
MkFile "$base/dao/inventory.py" @'
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.inventory import InventoryItem


class InventoryDAO:

    @staticmethod
    async def get_for_update(
        session: AsyncSession,
        *,
        operator_id: int,
        product_id: int,
    ) -> InventoryItem | None:
        stmt = (
            select(InventoryItem)
            .where(
                InventoryItem.operator_id == operator_id,
                InventoryItem.product_id == product_id,
            )
            .with_for_update()
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    def reserve(item: InventoryItem, qty: int):
        if item.quantity - item.reserved < qty:
            raise ValueError("not enough stock")
        item.reserved += qty

    @staticmethod
    def commit(item: InventoryItem, qty: int):
        item.quantity -= qty
        item.reserved -= qty

    @staticmethod
    def rollback(item: InventoryItem, qty: int):
        item.reserved -= qty
'@

# =========================================================
# 3. ACCEPT ORDER — ПРОВЕРКА ОСТАТКОВ
# =========================================================
MkFile "$base/services/order_inventory.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.inventory import InventoryDAO


async def reserve_order_items(
    session: AsyncSession,
    *,
    operator_id: int,
    items: list[tuple[int, int]],  # (product_id, qty)
):
    for product_id, qty in items:
        item = await InventoryDAO.get_for_update(
            session,
            operator_id=operator_id,
            product_id=product_id,
        )
        if not item:
            raise ValueError("item not found in inventory")

        InventoryDAO.reserve(item, qty)
'@

# =========================================================
# 4. СПИСАНИЕ ПРИ DONE
# =========================================================
MkFile "$base/services/inventory_commit.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.inventory import InventoryDAO


async def commit_order_items(
    session: AsyncSession,
    *,
    operator_id: int,
    items: list[tuple[int, int]],
):
    for product_id, qty in items:
        item = await InventoryDAO.get_for_update(
            session,
            operator_id=operator_id,
            product_id=product_id,
        )
        InventoryDAO.commit(item, qty)
'@

# =========================================================
# 5. ОНЛАЙН ОПЕРАТОРЫ
# =========================================================
MkFile "$base/services/online_operators.py" @'
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.operator_shift import OperatorShift, ShiftState


async def get_online_operators(session: AsyncSession):
    stmt = select(OperatorShift).where(OperatorShift.state == ShiftState.OPEN)
    res = await session.execute(stmt)
    return res.scalars().all()
'@

# =========================================================
# 6. SLA / AUTO CLOSE SHIFT
# =========================================================
MkFile "$base/services/operator_sla.py" @'
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.operator_shift import OperatorShift, ShiftState


WARN_1 = timedelta(minutes=15)
WARN_2 = timedelta(minutes=17)
WARN_3 = timedelta(minutes=18)
AUTO_CLOSE = timedelta(minutes=20)


async def get_inactive_shifts(session: AsyncSession):
    now = datetime.utcnow()

    stmt = select(OperatorShift).where(
        OperatorShift.state == ShiftState.OPEN
    )
    res = await session.execute(stmt)
    shifts = res.scalars().all()

    result = []
    for shift in shifts:
        delta = now - shift.opened_at
        result.append((shift, delta))

    return result
'@

Write-Host "Inventory + online operators + SLA system added." -ForegroundColor Green
