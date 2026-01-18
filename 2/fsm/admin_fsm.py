# bot/fsm/admin_fsm.py
from aiogram.fsm.state import State, StatesGroup

# bot/fsm/admin_fsm.py
from aiogram.fsm.state import State, StatesGroup








class AdminFSM(StatesGroup):


    idle = State()





    # === Operators ===


    managing_operators = State()


    op_tg_id = State()           # ввод TG ID оператора


    op_name = State()            # ввод имени оператора


    editing_operator = State()





    # === Products ===


    managing_products = State()


    product_title = State()


    product_price = State()


    editing_product = State()





    # === Warehouses ===


    managing_warehouses = State()


    wh_operator_tg_id = State()  # привязка склада к оператору


    wh_title = State()           # НАЗВАНИЕ склада


    wh_address = State()         # адрес склада / самовывоза


    editing_warehouse = State()





