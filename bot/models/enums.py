from __future__ import annotations

# bot/models/enums.py
from enum import StrEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class UserRole(StrEnum):
    ADMIN = auto()
    OPERATOR = auto()
    CLIENT = auto()


class OrderStatus(StrEnum):
    CART = auto()              # корзина
    WAITING_PAYMENT = auto()   # выбран способ оплаты
    NEED_CHECK = auto()        # чек отправлен, ждёт оператора
    PAID = auto()              # подтверждена
    IN_WORK = auto()           # у оператора
    READY = auto()             # готов
    DONE = auto()              # завершён


class OrderItemStatus(StrEnum):
    NEW = auto()
    ACCEPTED = auto()
    PAID = auto()
    DONE = auto()
    CANCELLED = auto()


class PaymentMethod(StrEnum):
    SBP = auto()
    BANK = auto()


class PaymentStatus(StrEnum):
    NEW = auto()
    SUBMITTED = auto()
    CONFIRMED = auto()
    REJECTED = auto()
# noqa: F821
