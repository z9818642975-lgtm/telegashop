from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.bank_event import BankEvent

class BankEventsDAO:
    def __init__(self, s: AsyncSession): self.s = s
    async def add(self, **data):
        e = BankEvent(**data)
        self.s.add(e); await self.s.flush()
        return e
