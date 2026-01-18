# bot/services/operator_items.py
from __future__ import annotations

from bot.dao.order_items import OrderItemDAO
from bot.dao.products_dao import ProductsDAO
from bot.dao.salary_dao import SalaryDAO


class OperatorItemService:
    """
    Р В¤Р С‘Р Р…Р В°Р В»Р С‘Р В·Р В°РЎвЂ Р С‘РЎРЏ OrderItem.

    Р вЂєР С•Р С–Р С‘Р С”Р В°:
    - Р С—Р ВµРЎР‚Р ВµР Р†Р С•Р Т‘ item Р Р† DONE
    - РЎР‚Р В°РЎРѓРЎвЂЎРЎвЂРЎвЂљ Р В·Р В°РЎР‚Р С—Р В»Р В°РЎвЂљРЎвЂ№ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎС“
    - РЎРЊРЎвЂљР С• Р С‘ Р ВµРЎРѓРЎвЂљРЎРЉ "РЎРѓР С—Р С‘РЎРѓР В°Р Р…Р С‘Р Вµ"
    """

    def __init__(self, session):
        self.items = OrderItemDAO(session)
        self.products = ProductsDAO   # РЎвЂ¦РЎР‚Р В°Р Р…Р С‘Р С Р С”Р В»Р В°РЎРѓРЎРѓ
        self.salary = SalaryDAO(session)
        self.session = session

    async def complete_with_salary(self, *, item_id: int):
        # 1РїС‘РЏРІС“Р€ Р С—Р ВµРЎР‚Р ВµР Р†Р С•Р Т‘Р С‘Р С Р С—Р С•Р В·Р С‘РЎвЂ Р С‘РЎР‹ Р Р† DONE
        item = await self.items.complete(item_id=item_id)

        # 2РїС‘РЏРІС“Р€ РЎРѓРЎвЂЎР С‘РЎвЂљР В°Р ВµР С Р В·Р В°РЎР‚Р С—Р В»Р В°РЎвЂљРЎС“
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

