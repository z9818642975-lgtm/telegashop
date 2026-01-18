from aiogram.fsm.state import StatesGroup, State


class OperatorPickupFSM(StatesGroup):
    comment = State()   # описание
    photo = State()     # фото

