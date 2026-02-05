# bot/dao/orders_dao.py
from datetime import datetime, timedelta

from sqlalchemy import select

from bot.dao.base import BaseDAO
from bot.dao.salary_dao import SalaryDAO
from bot.models import Order, OrderStatus


class OrdersDAO(BaseDAO):

    # =====================================================
    # CART
    # =====================================================

    async def get_or_create_cart(self, client_id: int) -> Order:
        res = await self.session.execute(
            select(Order).where(
                Order.client_id == client_id,
                Order.status == OrderStatus.CART,
            )
        )
        order = res.scalar_one_or_none()
        if order:
            return order

        order = Order(
            client_id=client_id,
            status=OrderStatus.CART,
        )
        self.session.add(order)
        await self.session.flush()
        return order

    # =====================================================
    # CHECKOUT → PAYMENT
    # =====================================================

    async def checkout(self, order_id: int, client_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if not order or order.client_id != client_id:
            raise ValueError("order not found")

        if order.status != OrderStatus.CART:
            raise ValueError("invalid state")

        order.status = OrderStatus.WAITING_PAYMENT
        await self.session.flush()

    # =====================================================
    # PAYMENT PROOF (ЧЕК)
    # =====================================================

    async def save_payment_proof(
        self,
        order_id: int,
        file_id: str,
        file_type: str,  # "photo" | "document"
    ) -> None:
        order = await self.session.get(Order, order_id)

        if order.status != OrderStatus.WAITING_PAYMENT:
            raise ValueError("invalid state")

        order.payment_proof_file_id = file_id
        order.payment_proof_type = file_type
        order.status = OrderStatus.NEED_CHECK
        order.payment_submitted_at = datetime.utcnow()

        await self.session.flush()

    # =====================================================
    # OPERATOR CONFIRMATION
    # =====================================================

    async def mark_paid(self, order_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if order.status != OrderStatus.NEED_CHECK:
            raise ValueError("invalid state")

        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()

        await self.session.flush()

    async def reject_payment(self, order_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if order.status != OrderStatus.NEED_CHECK:
            raise ValueError("invalid state")

        order.status = OrderStatus.WAITING_PAYMENT
        order.payment_proof_file_id = None
        order.payment_proof_type = None

        await self.session.flush()

    # =====================================================
    # OPERATOR FLOW
    # =====================================================

    async def assign_operator(self, order_id: int, operator_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if order.status != OrderStatus.PAID:
            raise ValueError("invalid state")

        order.operator_id = operator_id
        order.status = OrderStatus.IN_WORK
        order.sla_deadline = datetime.utcnow() + timedelta(minutes=30)

        await self.session.flush()

    async def mark_ready(self, order_id: int, operator_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if (
            order.operator_id != operator_id
            or order.status != OrderStatus.IN_WORK
        ):
            raise ValueError("invalid state")

        order.status = OrderStatus.READY
        await self.session.flush()

    async def mark_done(self, order_id: int, operator_id: int) -> None:
        order = await self.session.get(Order, order_id)

        if (
            order.operator_id != operator_id
            or order.status != OrderStatus.READY
        ):
            raise ValueError("invalid state")

        order.status = OrderStatus.DONE
        order.completed_at = datetime.utcnow()

        await self.session.flush()
        salary_dao = SalaryDAO(self.session)
        await salary_dao.create(
            operator_id=order.operator_id,
            amount=order.total_price,  # или % — по ТЗ
            order_id=order.id,
        )

    # =====================================================
    # SERVICE
    # =====================================================

    async def get_sla_expired(self, now: datetime) -> list[Order]:
        res = await self.session.execute(
            select(Order).where(
                Order.status == OrderStatus.IN_WORK,
                Order.sla_deadline < now,
            )
        )
        return list(res.scalars())

    async def get_active_order(self, client_id: int) -> Order | None:
        res = await self.session.execute(
            select(Order).where(
                Order.client_id == client_id,
                Order.status.in_(
                    [
                        OrderStatus.CART,
                        OrderStatus.WAITING_PAYMENT,
                        OrderStatus.NEED_CHECK,
                    ]
                ),
            )
        )
        return res.scalar_one_or_none()