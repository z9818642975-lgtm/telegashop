# bot/routers/common/guards.py
class GuardError(Exception):

# bot/routers/common/guards.py
class GuardError(Exception):


    pass








def guard_order_status(order, allowed: list[str]):


    if order.status not in allowed:


        raise GuardError("Р СњР ВµР Т‘Р С•Р С—РЎС“РЎРѓРЎвЂљР С‘Р СРЎвЂ№Р в„– РЎРѓРЎвЂљР В°РЎвЂљРЎС“РЎРѓ Р В·Р В°Р С”Р В°Р В·Р В°")








def guard_once(condition: bool, message: str):


    if condition:


        raise GuardError(message)





