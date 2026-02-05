# bot/fsm/checkout_fsm.py
from aiogram.fsm.state import State, StatesGroup


class CheckoutFSM(StatesGroup):
    delivery = State()

    pickup_comment = State()
    pickup_photo = State()

    address = State()

    payment = State()
    requisites = State()
    confirm = State()
    wait_check = State()


