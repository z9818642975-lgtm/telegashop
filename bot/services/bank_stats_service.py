from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.bank_events_dao import BankEventsDAO

class BankStatsService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.events = BankEventsDAO(s)

    async def shown(self, bank_id: int, account_id: int | None, order_id: int | None):
        await self.events.add(bank_id=bank_id, bank_account_id=account_id, order_id=order_id, event_type="SHOWN")

    async def paid(self, bank_id: int, account_id: int | None, order_id: int | None):
        await self.events.add(bank_id=bank_id, bank_account_id=account_id, order_id=order_id, event_type="PAID")

    async def timeout(self, bank_id: int, account_id: int | None, order_id: int | None):
        await self.events.add(bank_id=bank_id, bank_account_id=account_id, order_id=order_id, event_type="TIMEOUT")
