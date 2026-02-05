# bot/constants/callbacks_operator.py
from aiogram.filters.callback_data import CallbackData

# =========================================================
# OPERATOR — CHECK / DELIVERY
# =========================================================

class OperatorCheckCB(CallbackData, prefix="operator_check"):
    order_id: int
    result: str  # "paid" | "failed"


class OperatorDeliverySentCB(CallbackData, prefix="op_delivery_sent"):
    order_id: int

class OperatorDeliveryStartCB(CallbackData, prefix="op_delivery"):
    order_id: int

# =========================================================
# OPERATOR — SHIFT / HEARTBEAT
# =========================================================

class OperatorReady(CallbackData, prefix="operator_ready"):
    order_id: int


class OperatorHeartbeatCB(CallbackData, prefix="operator_heartbeat"):
    shift_id: int

class OperatorPickupStartCB(CallbackData, prefix="op_pickup"):
    order_id: int
# =========================================================
# OPERATOR — SALARY
# =========================================================

class OperatorSalaryStatsCB(CallbackData, prefix="op_salary_stats"):
    period: str  # day | week | month


class OperatorSalaryPayoutCB(CallbackData, prefix="op_salary_payout"):
    pass


# =========================================================
# OPERATOR — ITEMS / ORDERS
# =========================================================

class OperatorItemCB(CallbackData, prefix="op_item"):
    item_id: int


class OperatorOrdersCB(CallbackData, prefix="operator_orders"):
    action: str  # active | done