# bot/dao/payment.py
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order import Order
from bot.models.payment import Payment, PaymentStatus


class PaymentDAO:

    @staticmethod
    async def create_payment(
        session: AsyncSession,
        order_id: int,
        bank_id: int,
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            bank_id=bank_id,
            status=PaymentStatus.CREATED,
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment

    @staticmethod
    async def get_last_pending_payment(
        session: AsyncSession,
        user_id: int,
    ) -> Payment | None:
        stmt = (
            select(Payment)
            .join(Order)
            .where(
                Order.user_id == user_id,
                Payment.status.in_([
                    PaymentStatus.CREATED,
                    PaymentStatus.WAITING_CHECK,
                ])
            )
            .order_by(Payment.created_at.desc())
            .limit(1)
        )
        return await session.scalar(stmt)

    @staticmethod
    async def mark_waiting_check(
        session: AsyncSession,
        payment_id: int,
    ):
        await session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status=PaymentStatus.WAITING_CHECK)
        )
        await session.commit()


