# bot/fsm/admin_fsm.py
from aiogram.fsm.state import State, StatesGroup

# bot/fsm/admin_fsm.py
from aiogram.fsm.state import State, StatesGroup








class AdminFSM(StatesGroup):


    idle = State()





    # === Operators ===


    managing_operators = State()


    op_tg_id = State()           # Р Р†Р Р†Р С•Р Т‘ TG ID Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°


    op_name = State()            # Р Р†Р Р†Р С•Р Т‘ Р С‘Р СР ВµР Р…Р С‘ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°


    editing_operator = State()





    # === Products ===


    managing_products = State()


    product_title = State()


    product_price = State()


    editing_product = State()





    # === Warehouses ===


    managing_warehouses = State()


    wh_operator_tg_id = State()  # Р С—РЎР‚Р С‘Р Р†РЎРЏР В·Р С”Р В° РЎРѓР С”Р В»Р В°Р Т‘Р В° Р С” Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎС“


    wh_title = State()           # Р СњР С’Р вЂ”Р вЂ™Р С’Р СњР ВР вЂў РЎРѓР С”Р В»Р В°Р Т‘Р В°


    wh_address = State()         # Р В°Р Т‘РЎР‚Р ВµРЎРѓ РЎРѓР С”Р В»Р В°Р Т‘Р В° / РЎРѓР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В·Р В°


    editing_warehouse = State()





