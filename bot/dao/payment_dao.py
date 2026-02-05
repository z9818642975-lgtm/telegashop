# bot/dao/payment_dao.py
from sqlalchemy import select

from bot.dao.base import BaseDAO
from bot.models.enums import PaymentStatus
from bot.models.payment import Payment


class PaymentDAO(BaseDAO):

    async def create_payment(self, order_id: int, method: str) -> Payment:
        res = await self.session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        payment = res.scalar_one_or_none()
        if payment:
            return payment

        payment = Payment(
            order_id=order_id,
            method=method,
            status=PaymentStatus.WAITING,
        )
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def mark_paid(self, order_id: int) -> None:
        res = await self.session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        payment = res.scalar_one_or_none()
        if payment:
            payment.status = PaymentStatus.PAID
