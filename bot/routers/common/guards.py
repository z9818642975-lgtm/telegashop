# bot/routers/common/guards.py
class GuardError(Exception):

# bot/routers/common/guards.py
class GuardError(Exception):


    pass








def guard_order_status(order, allowed: list[str]):


    if order.status not in allowed:


        raise GuardError("Недопустимый статус заказа")








def guard_once(condition: bool, message: str):


    if condition:


        raise GuardError(message)





