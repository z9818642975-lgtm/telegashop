# bot/dao/payment_dao.py

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.payment import Payment
from bot.models.bank_account import BankAccount



class PaymentDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, payment_id: int) -> Payment | None:
        res = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return res.scalar_one_or_none()

    async def attach_proof(
        self,
        *,
        payment_id: int,
        file_id: str,
    ) -> None:
        await self.session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(proof_file_id=file_id)
        )
        await self.session.flush()

    async def list_requisites(self):
        result = await self.session.scalars(
            select(BankAccount).where(BankAccount.is_active == True)
        )
        return result.all()

        result = await self.session.execute(
            select(PaymentRequisite)
        )
        return result.scalars().all()


    
    async def approve_by_operator(
        self,
        *,
        payment_id: int,
        operator_tg_id: int,
    ) -> None:
        payment = await self.session.get(Payment, payment_id)
        if not payment:
            raise NotFoundError("Платёж не найден")

        if payment.status != PaymentStatus.ON_REVIEW:
            raise InvalidStateError("Платёж не на проверке")

        payment.status = PaymentStatus.APPROVED
        payment.approved_at = datetime.utcnow()
        payment.approved_by_operator_id = operator_tg_id

        await self.session.flush()


    async def reject_by_operator(
        self,
        *,
        payment_id: int,
        operator_tg_id: int,
        reason: str,
        disable_minutes: int | None = None,
    ) -> None:
        payment = await self.session.get(Payment, payment_id)
        if not payment:
            raise NotFoundError("Платёж не найден")

        payment.status = PaymentStatus.REJECTED
        payment.reject_reason = reason
        payment.rejected_at = datetime.utcnow()
        payment.rejected_by_operator_id = operator_tg_id

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

