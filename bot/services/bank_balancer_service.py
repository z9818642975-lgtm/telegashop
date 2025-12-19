from __future__ import annotations
import random
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.banks_dao import BanksDAO

class BankBalancerService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.banks = BanksDAO(s)

    async def pick_account(self, bank_id: int):
        accounts = await self.banks.list_active_accounts(bank_id)
        now = datetime.utcnow()
        accounts = [a for a in accounts if not a.disabled_until or a.disabled_until < now]
        if not accounts:
            raise ValueError("Нет доступных реквизитов")

        population = []
        for a in accounts:
            population.extend([a] * max(int(a.weight or 1), 1))
        return random.choice(population)

    async def penalize(self, account_id: int, minutes: int = 30):
        await self.banks.disable_temporarily(account_id, minutes)
