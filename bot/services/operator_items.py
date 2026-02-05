# bot/services/operator_items.py
from __future__ import annotations

from bot.dao.order_items import OrderItemDAO
from bot.dao.products_dao import ProductsDAO
from bot.dao.salary_dao import SalaryDAO


class OperatorItemService:
    """
    Финализация OrderItem.

    Логика:
    - перевод item в DONE
    - расчёт зарплаты оператору
    - это и есть "списание"
    """

    def __init__(self, session):
        self.items = OrderItemDAO(session)
        self.products = ProductsDAO   # храним класс
        self.salary = SalaryDAO(session)
        self.session = session

    async def complete_with_salary(self, *, item_id: int):
        # 1️⃣ переводим позицию в DONE
        item = await self.items.complete(item_id=item_id)

        # 2️⃣ считаем зарплату
        product = await self.products.get_by_id(item.product_id)
        if not product:
            raise ValueError("Product not found")

        amount = product.base_price * item.qty

        await self.salary.create(
            operator_id=item.operator_id,
            order_id=item.order_id,
            amount=amount,
        )

        return item



