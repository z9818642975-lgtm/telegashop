from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.stock_reservation import StockReservation

class ReservationsDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def create(self, **data):
        r = StockReservation(**data)
        self.s.add(r); await self.s.flush()
        return r

    async def list_by_order(self, order_id: int):
        res = await self.s.execute(select(StockReservation).where(StockReservation.order_id==order_id))
        return res.scalars().all()
