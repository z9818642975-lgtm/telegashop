$base = "bot_refactored_v2"

if (Test-Path $base) {
    Write-Host "Directory '$base' already exists. Aborting." -ForegroundColor Red
    exit 1
}

function MkDir($p) { New-Item -ItemType Directory -Path $p | Out-Null }
function MkFile($p, $c) {
    $d = Split-Path $p
    if (-not (Test-Path $d)) { MkDir $d }
    Set-Content -Path $p -Value $c -Encoding UTF8
}

# ----------------- DIRS -----------------
MkDir $base
MkDir "$base/app/operator_shift"
MkDir "$base/app/orders"
MkDir "$base/app/payments"
MkDir "$base/domain"
MkDir "$base/dao"
MkDir "$base/models"
MkDir "$base/services"
MkDir "$base/fsm"

# ----------------- MODELS -----------------
MkFile "$base/models/audit_log.py" @'
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from bot_refactored.db import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None]
    action: Mapped[str]
    entity: Mapped[str]
    entity_id: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
'@

# ----------------- DOMAIN -----------------
MkFile "$base/domain/payment.py" @'
class PaymentStateError(Exception):
    pass
'@

# ----------------- DAO -----------------
MkFile "$base/dao/audit_log.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.audit_log import AuditLog

class AuditLogDAO:
    @staticmethod
    async def write(
        session: AsyncSession,
        *,
        actor_id: int | None,
        action: str,
        entity: str,
        entity_id: int | None,
    ):
        session.add(
            AuditLog(
                actor_id=actor_id,
                action=action,
                entity=entity,
                entity_id=entity_id,
            )
        )
'@

# ----------------- PAYMENTS -----------------
MkFile "$base/app/payments/pay_order.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.dao.audit_log import AuditLogDAO
from bot_refactored.models.order import OrderStatus

class PayOrderUseCase:
    def __init__(self, *, order_id: int, session: AsyncSession):
        self.order_id = order_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            if order.status == OrderStatus.PAID:
                return  # идемпотентность

            if order.status != OrderStatus.ACCEPTED:
                raise ValueError("invalid order state")

            await OrdersDAO.mark_paid(order)

            await AuditLogDAO.write(
                self.session,
                actor_id=None,
                action="ORDER_PAID",
                entity="order",
                entity_id=order.id,
            )
'@

# ----------------- FSM CONTROLLER -----------------
MkFile "$base/fsm/controller.py" @'
class FSMController:
    def __init__(self, state):
        self.state = state

    async def finish(self):
        await self.state.clear()

    async def reset_and_start(self, new_state):
        await self.state.clear()
        await self.state.set_state(new_state)
'@

# ----------------- SERVICES -----------------
MkFile "$base/services/fsm_guard.py" @'
class FSMAbort(Exception):
    pass
'@

# ----------------- README (якорь) -----------------
MkFile "$base/README.md" @'
bot_refactored — архитектурный слой.

Правила:
- routers НЕ содержат бизнес-логики
- domain запрещает невозможное
- use cases управляют транзакциями
- DAO только БД
- все внешние события идемпотентны

Этот каталог — ЭТАЛОН.
'@

Write-Host "bot_refactored created: payments + audit + FSM controller included." -ForegroundColor Green
