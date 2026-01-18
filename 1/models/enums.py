from enum import StrEnum, auto


class UserRole(StrEnum):
    ADMIN = auto()
    OPERATOR = auto()
    CLIENT = auto()


class OrderStatus(StrEnum):
    NEW = auto()                 # Р С”Р С•РЎР‚Р В·Р С‘Р Р…Р В°
    WAITING_PAYMENT = auto()     # Р С•Р В¶Р С‘Р Т‘Р В°Р ВµР С Р С•Р С—Р В»Р В°РЎвЂљРЎС“
    PAYMENT_SUBMITTED = auto()   # РЎвЂЎР ВµР С” Р С•РЎвЂљР С—РЎР‚Р В°Р Р†Р В»Р ВµР Р…
    ASSEMBLING = auto()          # Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ РЎРѓР С•Р В±Р С‘РЎР‚Р В°Р ВµРЎвЂљ
    READY = auto()               # Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р В·Р В°Р С–РЎР‚РЎС“Р В·Р С‘Р В» РЎвЂћР С•РЎвЂљР С• + Р С•Р С—Р С‘РЎРѓР В°Р Р…Р С‘Р Вµ
    SENT = auto()                # Р Т‘Р С•РЎРѓРЎвЂљР В°Р Р†Р С”Р В° Р С•РЎвЂљР С—РЎР‚Р В°Р Р†Р В»Р ВµР Р…Р В°
    PICKED_UP = auto()           # РЎРѓР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В· Р В·Р В°Р В±РЎР‚Р В°Р Р…
    DONE = auto()
    CANCELLED = auto()


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

