$base = "bot_refactored"

if (Test-Path $base) {
    Write-Host "Directory '$base' already exists. Aborting." -ForegroundColor Red
    exit 1
}

# ---------- helpers ----------
function MkDir($path) {
    New-Item -ItemType Directory -Path $path | Out-Null
}

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) { MkDir $dir }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ---------- dirs ----------
MkDir "$base"
MkDir "$base/app/operator_shift"
MkDir "$base/app/orders"
MkDir "$base/domain"
MkDir "$base/dao"
MkDir "$base/models"

# ---------- models ----------
MkFile "$base/models/operator_shift.py" @'
from __future__ import annotations

from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot_refactored.db import Base


class ShiftState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class OperatorShift(Base):
    __tablename__ = "operator_shifts"

    id: Mapped[int] = mapped_column(primary_key=True)
    operator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    state: Mapped[ShiftState] = mapped_column(
        SAEnum(ShiftState),
        default=ShiftState.CLOSED,
        nullable=False,
    )
    opened_at: Mapped[datetime | None]
    closed_at: Mapped[datetime | None]
    pickup_address: Mapped[str | None]
'@

MkFile "$base/models/order.py" @'
from __future__ import annotations

from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot_refactored.db import Base


class OrderStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    PAID = "paid"
    DONE = "done"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    shift_id: Mapped[int | None] = mapped_column(ForeignKey("operator_shifts.id"))

    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus),
        default=OrderStatus.NEW,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    paid_at: Mapped[datetime | None]
    completed_at: Mapped[datetime | None]
'@

# ---------- domain ----------
MkFile "$base/domain/operator_shift.py" @'
from bot_refactored.models.operator_shift import ShiftState


class ShiftStateError(Exception):
    pass


class OperatorShiftDomain:
    def __init__(self, state: ShiftState):
        self.state = state

    def can_open(self) -> None:
        if self.state == ShiftState.OPEN:
            raise ShiftStateError("shift already open")

    def can_close(self) -> None:
        if self.state == ShiftState.CLOSED:
            raise ShiftStateError("shift already closed")
'@

MkFile "$base/domain/order.py" @'
from bot_refactored.models.order import OrderStatus


class OrderStateError(Exception):
    pass


class OrderDomain:
    ALLOWED = {
        OrderStatus.NEW: {OrderStatus.ACCEPTED},
        OrderStatus.ACCEPTED: {OrderStatus.PAID},
        OrderStatus.PAID: {OrderStatus.DONE},
        OrderStatus.DONE: set(),
    }

    def __init__(self, status: OrderStatus):
        self.status = status

    def can_transition(self, to: OrderStatus) -> None:
        if to not in self.ALLOWED[self.status]:
            raise OrderStateError(f"invalid transition {self.status} -> {to}")
'@

# ---------- dao ----------
MkFile "$base/dao/operator_shift.py" @'
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.operator_shift import OperatorShift, ShiftState


class OperatorShiftDAO:

    @staticmethod
    async def get_active_for_update(session: AsyncSession, operator_id: int):
        stmt = (
            select(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.state == ShiftState.OPEN,
            )
            .with_for_update()
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def create_open(session: AsyncSession, operator_id: int, address: str):
        shift = OperatorShift(
            operator_id=operator_id,
            state=ShiftState.OPEN,
            opened_at=datetime.utcnow(),
            pickup_address=address,
        )
        session.add(shift)
        return shift

    @staticmethod
    async def close(shift: OperatorShift):
        shift.state = ShiftState.CLOSED
        shift.closed_at = datetime.utcnow()
'@

MkFile "$base/dao/orders.py" @'
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.order import Order, OrderStatus


class OrdersDAO:

    @staticmethod
    async def get_for_update(session: AsyncSession, order_id: int):
        stmt = select(Order).where(Order.id == order_id).with_for_update()
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def accept(order: Order, operator_id: int, shift_id: int):
        order.operator_id = operator_id
        order.shift_id = shift_id
        order.status = OrderStatus.ACCEPTED

    @staticmethod
    async def mark_paid(order: Order):
        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()

    @staticmethod
    async def complete(order: Order):
        order.status = OrderStatus.DONE
        order.completed_at = datetime.utcnow()
'@

# ---------- app / operator_shift ----------
MkFile "$base/app/operator_shift/open_shift.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.operator_shift import OperatorShiftDomain


class OpenShiftUseCase:
    def __init__(self, operator_id: int, pickup_address: str, session: AsyncSession):
        self.operator_id = operator_id
        self.pickup_address = pickup_address
        self.session = session

    async def execute(self):
        async with self.session.begin():
            active = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if active:
                OperatorShiftDomain(active.state).can_open()

            await OperatorShiftDAO.create_open(
                self.session, self.operator_id, self.pickup_address
            )
'@

MkFile "$base/app/operator_shift/close_shift.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.operator_shift import OperatorShiftDomain, ShiftStateError


class CloseShiftUseCase:
    def __init__(self, operator_id: int, session: AsyncSession):
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            shift = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if not shift:
                raise ShiftStateError("no active shift")

            OperatorShiftDomain(shift.state).can_close()
            await OperatorShiftDAO.close(shift)
'@

# ---------- app / orders ----------
MkFile "$base/app/orders/accept_order.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.order import OrderDomain


class AcceptOrderUseCase:
    def __init__(self, order_id: int, operator_id: int, session: AsyncSession):
        self.order_id = order_id
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            shift = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if not shift:
                raise PermissionError("no active shift")

            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            OrderDomain(order.status).can_transition(order.status.ACCEPTED)  # type: ignore
            await OrdersDAO.accept(order, self.operator_id, shift.id)
'@

MkFile "$base/app/orders/pay_order.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class PayOrderUseCase:
    def __init__(self, order_id: int, session: AsyncSession):
        self.order_id = order_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            if order.status == OrderStatus.PAID:
                return

            OrderDomain(order.status).can_transition(OrderStatus.PAID)
            await OrdersDAO.mark_paid(order)
'@

MkFile "$base/app/orders/complete_order.py" @'
from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.orders import OrdersDAO
from bot_refactored.domain.order import OrderDomain
from bot_refactored.models.order import OrderStatus


class CompleteOrderUseCase:
    def __init__(self, order_id: int, operator_id: int, session: AsyncSession):
        self.order_id = order_id
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            order = await OrdersDAO.get_for_update(self.session, self.order_id)
            if not order:
                raise ValueError("order not found")

            if order.status == OrderStatus.DONE:
                return

            if order.operator_id != self.operator_id:
                raise PermissionError("not your order")

            OrderDomain(order.status).can_transition(OrderStatus.DONE)
            await OrdersDAO.complete(order)
'@

Write-Host "bot_refactored created with full architecture and code." -ForegroundColor Green
