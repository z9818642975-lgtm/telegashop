# bot/services/operator_guard.py
from __future__ import annotations

from bot.dao.order_items import OrderItemDAO
from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.exceptions import ForbiddenError


async def ensure_operator_owns_item(
    *,
    operator_id: int,
    item_id: int,
    session,
) -> None:
    """
    Р вЂњР В°РЎР‚Р В°Р Р…РЎвЂљР С‘РЎР‚РЎС“Р ВµРЎвЂљ, РЎвЂЎРЎвЂљР С•:
    1) Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р Р…Р В°РЎвЂ¦Р С•Р Т‘Р С‘РЎвЂљРЎРѓРЎРЏ Р Р…Р В° Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•Р в„– РЎРѓР СР ВµР Р…Р Вµ
    2) OrderItem Р С—РЎР‚Р С‘Р Р…Р В°Р Т‘Р В»Р ВµР В¶Р С‘РЎвЂљ РЎРЊРЎвЂљР С•Р СРЎС“ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎС“
    """

    shifts = OperatorShiftDAO(session)

    if not await shifts.is_on_shift(operator_id):
        raise ForbiddenError("Operator is not on active shift")

    items = OrderItemDAO(session)
    item = await items.get_by_id(item_id)

    if not item:
        raise ForbiddenError("OrderItem not found")

    if item.operator_id != operator_id:
        raise ForbiddenError("OrderItem does not belong to operator")

