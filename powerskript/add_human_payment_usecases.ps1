$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ---------- SubmitPaymentProofUseCase ----------
MkFile "$base/app/orders/submit_payment_proof.py" @'
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class SubmitPaymentProofUseCase:
    def __init__(
        self,
        *,
        order_id: int,
        client_id: int,
        photo_id: str,
        comment: str | None,
        session: AsyncSession,
    ):
        self.order_id = order_id
        self.client_id = client_id
        self.photo_id = photo_id
        self.comment = comment
        self.session = session

    async def execute(self) -> None:
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(
                self.session,
                self.order_id,
            )
            if not order:
                raise ValueError("order not found")

            if order.client_id != self.client_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(
                OrderStatus.WAITING_CONFIRMATION
            )

            order.payment_photo_id = self.photo_id
            order.payment_comment = self.comment
            order.status = OrderStatus.WAITING_CONFIRMATION
'@

# ---------- ConfirmPaymentUseCase ----------
MkFile "$base/app/orders/confirm_payment.py" @'
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class ConfirmPaymentUseCase:
    def __init__(
        self,
        *,
        order_id: int,
        operator_id: int,
        session: AsyncSession,
    ):
        self.order_id = order_id
        self.operator_id = operator_id
        self.session = session

    async def execute(self) -> None:
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(
                self.session,
                self.order_id,
            )
            if not order:
                raise ValueError("order not found")

            if order.operator_id != self.operator_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(
                OrderStatus.PAID
            )

            order.status = OrderStatus.PAID
'@

Write-Host "Human-in-the-loop payment use cases created." -ForegroundColor Green
