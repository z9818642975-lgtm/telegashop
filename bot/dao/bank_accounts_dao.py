from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.bank_account import BankAccount


class BankAccountsDAO:
    """
    DAO для работы с банковскими реквизитами.

    Используется на этапе оплаты:
    - выбор банка
    - получение реквизитов
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, bank_id: int) -> BankAccount | None:
        """
        Получить банк по ID.
        """
        res = await self.session.execute(
            select(BankAccount).where(BankAccount.id == bank_id)
        )
        return res.scalar_one_or_none()

    async def list_active(self) -> list[BankAccount]:
        """
        Получить список активных банков.
        """
        res = await self.session.execute(
            select(BankAccount)
            .where(BankAccount.is_active.is_(True))
            .order_by(BankAccount.id)
        )
        return list(res.scalars().all())
