# bot/dao/bank_accounts_dao.py
from bot.dao.base import BaseDAO
from bot.models import BankAccount


class BankAccountsDAO(BaseDAO):

    async def toggle(self, bank_id: int):
        bank = await self.session.get(BankAccount, bank_id)
        bank.is_active = not bank.is_active
