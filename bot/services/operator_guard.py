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
    Гарантирует, что:
    1) оператор находится на активной смене
    2) OrderItem принадлежит этому оператору
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

