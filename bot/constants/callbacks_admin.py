# bot/constants/callbacks_admin.py
from aiogram.filters.callback_data import CallbackData

# =========================
# PRODUCTS
# =========================

class AdminProducts(CallbackData, prefix="admin_products"):
    pass


class AdminProductCard(CallbackData, prefix="admin_product_card"):
    product_id: int


class AdminProductToggle(CallbackData, prefix="admin_product_toggle"):
    product_id: int


# =========================
# BANKS
# =========================

class AdminBanks(CallbackData, prefix="admin_banks"):
    pass


class AdminBankToggle(CallbackData, prefix="admin_bank_toggle"):
    bank_id: int


# =========================
# OPERATORS
# =========================

class AdminOperators(CallbackData, prefix="admin_operators"):
    pass


class AdminOperatorToggle(CallbackData, prefix="admin_operator_toggle"):
    operator_id: int


# =========================
# WAREHOUSES
# =========================

class AdminWarehousesListCB(CallbackData, prefix="admin_wh_list"):
    pass


class AdminWarehouseSelectCB(CallbackData, prefix="admin_wh_select"):
    warehouse_id: int


class AdminWarehouseProductsCB(CallbackData, prefix="admin_wh_products"):
    warehouse_id: int


class AdminWarehouseMoveCB(CallbackData, prefix="admin_wh_move"):
    warehouse_id: int


class AdminWarehouseDeactivateCB(CallbackData, prefix="admin_wh_deactivate"):
    warehouse_id: int


# =========================
# ORDERS (ЕДИНЫЙ КОНТУР)
# =========================

class AdminOrders(CallbackData, prefix="admin_orders"):
    page: int = 1
    status: str | None = None
    order_id: int | None = None
    view: str | None = None


class AdminOrderForce(CallbackData, prefix="admin_order_force"):
    order_id: int


# =========================
# SALARY
# =========================

class AdminSalaryMenuCB(CallbackData, prefix="admin_salary"):
    pass


class AdminSalaryPayCB(CallbackData, prefix="admin_salary_pay"):
    accrual_id: int

    

