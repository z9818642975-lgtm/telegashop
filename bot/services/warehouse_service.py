# bot/services/warehouse_service.py
from __future__ import annotations


class WarehouseService:
    """
    DEPRECATED.

    Складская модель выведена из бизнес-логики.
    Списание товара происходит логически
    через завершение OrderItem (status = DONE).

    Файл оставлен как заглушка для совместимости,
    чтобы не ломать импорты.
    """

    @staticmethod
    async def writeoff_order(*args, **kwargs) -> None:
        # intentionally disabled
        return

