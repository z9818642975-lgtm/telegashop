$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# =========================================================
# 1. ОТКЛОНЕНИЕ ОПЛАТЫ
# =========================================================
MkFile "$base/app/orders/reject_payment.py" @'
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class RejectPaymentUseCase:
    def __init__(
        self,
        *,
        order_id: int,
        operator_id: int,
        reason: str,
        session: AsyncSession,
    ):
        self.order_id = order_id
        self.operator_id = operator_id
        self.reason = reason
        self.session = session

    async def execute(self) -> None:
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(
                self.session, self.order_id
            )
            if not order:
                raise ValueError("order not found")

            if order.operator_id != self.operator_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(
                OrderStatus.ACCEPTED
            )

            order.payment_comment = self.reason
            order.payment_photo_id = None
            order.status = OrderStatus.ACCEPTED
'@

# =========================================================
# 2. SLA-ТАЙМЕР ОЖИДАНИЯ ПОДТВЕРЖДЕНИЯ
# =========================================================
MkFile "$base/services/payment_sla.py" @'
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.order import Order, OrderStatus


SLA_HOURS = 2  # можно менять


async def get_expired_payment_orders(session: AsyncSession):
    deadline = datetime.utcnow() - timedelta(hours=SLA_HOURS)

    stmt = select(Order).where(
        Order.status == OrderStatus.WAITING_CONFIRMATION,
        Order.created_at <= deadline,
    )

    result = await session.execute(stmt)
    return result.scalars().all()
'@

# =========================================================
# 3. КАРТОЧКА ЗАКАЗА ОПЕРАТОРУ С ЧЕКОМ
# =========================================================
MkFile "$base/services/operator_order_card.py" @'
from bot_refactored.models.order import Order


def render_operator_order_card(order: Order) -> str:
    lines = [
        f"Заказ #{order.id}",
        f"Статус: {order.status}",
    ]

    if order.payment_photo_id:
        lines.append("Чек: приложен")
    else:
        lines.append("Чек: отсутствует")

    if order.payment_comment:
        lines.append(f"Комментарий: {order.payment_comment}")

    return "\n".join(lines)
'@

# =========================================================
# 4. AUDIT-LOG ПОДТВЕРЖДЕНИЙ / ОТКЛОНЕНИЙ
# =========================================================
MkFile "$base/services/payment_audit.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.audit_log import AuditLogDAO


async def log_payment_event(
    session: AsyncSession,
    *,
    actor_id: int,
    action: str,
    order_id: int,
):
    await AuditLogDAO.write(
        session,
        actor_id=actor_id,
        action=action,
        entity="order",
        entity_id=order_id,
    )
'@

Write-Host "Payment controls added: reject + SLA + card + audit" -ForegroundColor Green
