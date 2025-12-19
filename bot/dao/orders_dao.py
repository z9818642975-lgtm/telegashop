from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.order import Order

class OrdersDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get(self, order_id: int) -> Order:
        res = await self.s.execute(select(Order).where(Order.id==order_id))
        return res.scalar_one()

    async def create(self, **data) -> Order:
        o = Order(**data)
        self.s.add(o); await self.s.flush()
        return o

    async def set_status(self, order_id: int, status: str):
        await self.s.execute(update(Order).where(Order.id==order_id).values(status=status))

    async def attach_payment_choice(self, order_id: int, bank_id: int, bank_account_id: int):
        await self.s.execute(update(Order).where(Order.id==order_id).values(bank_id=bank_id, bank_account_id=bank_account_id))

    async def set_delivery(self, order_id: int, method: str, fee: int = 0, shift_id=None, operator_id=None, pickup_addr=None):
        await self.s.execute(update(Order).where(Order.id==order_id).values(
            delivery_method=method, delivery_fee=fee, shift_id=shift_id, operator_id=operator_id, pickup_address_snapshot=pickup_addr
        ))

    async def reassign_pickup(self, order_id: int, operator_id: int, shift_id: int, pickup_addr: str):
        await self.s.execute(update(Order).where(Order.id==order_id).values(operator_id=operator_id, shift_id=shift_id, pickup_address_snapshot=pickup_addr))

    async def list_by_status(self, status: str):
        res = await self.s.execute(select(Order).where(Order.status==status).order_by(Order.id.desc()))
        return res.scalars().all()
