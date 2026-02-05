# bot/fsm/order_fsm.py
# bot/fsm/order.py
# bot/fsm/order.py


from aiogram.fsm.state import State, StatesGroup


class OrderFSM(StatesGroup):


    delivery_type = State()


    address = State()


    payment_bank = State()


    wait_check = State()






