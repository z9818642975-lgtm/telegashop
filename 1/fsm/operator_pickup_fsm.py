from aiogram.fsm.state import StatesGroup, State


class OperatorPickupFSM(StatesGroup):
    comment = State()   # Р С•Р С—Р С‘РЎРѓР В°Р Р…Р С‘Р Вµ
    photo = State()     # РЎвЂћР С•РЎвЂљР С•

