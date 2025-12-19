from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.payment import Payment

class PaymentsDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get(self, order_id: int) -> Payment | None:
        res = await self.s.execute(select(Payment).where(Payment.order_id==order_id))
        return res.scalar_one_or_none()

    async def create_or_update_proof(self, order_id: int, file_id: str):
        p = await self.get(order_id)
        if p:
            p.proof_file_id = file_id
        else:
            p = Payment(order_id=order_id, proof_file_id=file_id, is_confirmed=False)
            self.s.add(p); await self.s.flush()
        return p

    async def confirm(self, order_id: int, operator_tg_id: int):
        await self.s.execute(update(Payment).where(Payment.order_id==order_id).values(is_confirmed=True, confirmed_by_operator_id=operator_tg_id))
