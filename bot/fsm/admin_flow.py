# bot/fsm/admin_flow.py
from aiogram.fsm.state import State, StatesGroup

# bot/fsm/admin_flow.py





class AdminFSM(StatesGroup):


    # create operator


    op_tg_id = State()


    op_name = State()





    # create operator warehouse (optional)


    wh_operator_tg_id = State()


    wh_title = State()


    wh_address = State()





    # edit address


    wh_set_address = State()





    # transfer


    tr_from_wh = State()


    tr_to_wh = State()


    tr_product_id = State()


    tr_qty = State()






