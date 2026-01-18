from aiogram.fsm.state import StatesGroup, State


class CheckoutFSM(StatesGroup):
    delivery = State()

    pickup_comment = State()
    pickup_photo = State()

    address = State()

    payment = State()
    requisites = State()
    confirm = State()
    wait_check = State()

