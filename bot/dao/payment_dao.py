from datetime import datetime, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.payment import Payment
from bot.models.bank_account import BankAccount
from bot.models.enums import PaymentStatus


class PaymentDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, payment_id: int) -> Payment | None:
        res = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return res.scalar_one_or_none()

    async def attach_check(
        self,
        *,
        payment_id: int,
        file_id: str,
    ) -> None:
        await self.session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(check_file_id=file_id)
        )
        await self.session.flush()

    async def list_requisites(self) -> list[BankAccount]:
        res = await self.session.execute(
            select(BankAccount)
            .where(BankAccount.is_active == True)
        )
        return res.scalars().all()

    async def approve(
        self,
        *,
        payment_id: int,
    ) -> None:
        await self.session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(
                status=PaymentStatus.APPROVED,
                approved_at=datetime.utcnow(),
            )
        )
        await self.session.flush()

    async def reject(
        self,
        *,
        payment_id: int,
        reason: str,
        disable_minutes: int | None = None,
    ) -> None:
        payment = await self.get_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        await self.session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(
                status=PaymentStatus.REJECTED,
                reject_reason=reason,
                rejected_at=datetime.utcnow(),
            )
        )

        if disable_minutes:
            await self.session.execute(
                update(BankAccount)
                .where(BankAccount.id == payment.bank_account_id)
                .values(
                    disabled_until=datetime.utcnow()
                    + timedelta(minutes=disable_minutes)
                )
            )

        await self.session.flush()
