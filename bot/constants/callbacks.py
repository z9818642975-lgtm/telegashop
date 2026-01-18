class CB:
    # ===== common =====
    BACK_MENU = "back:menu"
    BACK_CATALOG = "back:catalog"

    # ===== catalog =====
    CATALOG_OPEN = "catalog:open"
    PRODUCT_OPEN = "product:open"      # product:open:<product_id>
    PRODUCT_ADD = "product:add"        # product:add:<product_id>

    # ===== cart =====
    CART_OPEN = "cart:open"
    CART_CLEAR = "cart:clear"
    CART_CHECKOUT = "cart:checkout"

    # item-level (НЕ enum-шаблоны, а префиксы)
    ITEM_QTY = "item:qty"              # item:qty:<order_item_id>:<qty>
    ITEM_REMOVE = "item:remove"        # item:remove:<order_item_id>

    # ===== delivery =====
    DELIVERY_PICKUP = "delivery:pickup"
    DELIVERY_COURIER = "delivery:courier"

    # ===== payment =====
    PAY_BANK = "pay:bank"              # pay:bank:<bank_id>
    PAY_SBP = "pay:sbp"
    PAYMENT_DONE = "payment:done"
    PAYMENT_CANCEL = "payment:cancel"

    # ===== operator =====
    OP_ALIVE = "op:alive"
    OP_SHIFT_START = "op:shift:start"
    OP_SHIFT_CONFIRM = "op:shift:confirm"
    OP_SHIFT_CANCEL = "op:shift:cancel"
    OP_SHIFT_STOP = "op:shift:stop"
    OP_SHIFT_EDIT_ADDRESS = "op:shift:edit_address"

    OP_CHECK_ACCEPT = "op:order:accept"  # :<order_id>
    OP_READY = "op:order:ready"          # :<order_id>
    OP_SENT = "op:order:sent"            # :<order_id>

    # ===== admin =====
    ADMIN_PRODUCTS = "admin:products"
    ADMIN_WAREHOUSES = "admin:warehouses"
    ADMIN_OPERATORS = "admin:operators"
