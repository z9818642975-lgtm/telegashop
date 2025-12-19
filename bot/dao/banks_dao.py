from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from bot.models.bank_account import BankAccount

class BanksDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def list_active_accounts(self, bank_id: int):
        res = await self.s.execute(select(BankAccount).where(BankAccount.bank_id==bank_id, BankAccount.is_active.is_(True)).order_by(BankAccount.load.asc()))
        return res.scalars().all()

    async def disable_temporarily(self, account_id: int, minutes: int):
        until = datetime.utcnow() + timedelta(minutes=minutes)
        await self.s.execute(update(BankAccount).where(BankAccount.id==account_id).values(disabled_until=until))
