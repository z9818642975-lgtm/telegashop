from enum import Enum


class OperatorAction(str, Enum):
    SHIFT_START = "operator.shift.start"
    SHIFT_STOP = "operator.shift.stop"
    ORDERS_ACTIVE = "operator.orders.active"