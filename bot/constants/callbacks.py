class CB:
    # =====================================================
    # COMMON
    # =====================================================
    BACK_MENU = "common:back:menu"
    BACK_CATALOG = "common:back:catalog"

    # =====================================================
    # CLIENT — CATALOG
    # =====================================================
    CATALOG_OPEN = "catalog:open"
    PRODUCT_OPEN = "client:product:open"     # :<product_id>
    PRODUCT_ADD = "client:product:add"       # :<product_id>

    # =====================================================
    # CLIENT — CART
    # =====================================================
    CLIENT_CART_OPEN = "client:cart:open"
    CLIENT_CART_CLEAR = "client:cart:clear"
    CLIENT_CART_CHECKOUT = "client:cart:checkout"

    ITEM_QTY = "item:qty"                     # item:qty:<order_item_id>:<qty>
    ITEM_REMOVE = "item:remove"               # item:remove:<order_item_id>

    # =====================================================
    # CLIENT — DELIVERY
    # =====================================================
    CLIENT_DELIVERY_PICKUP = "client:delivery:pickup"
    CLIENT_DELIVERY_COURIER = "client:delivery:courier"

    # =====================================================
    # CLIENT — PAYMENT
    # =====================================================
    CLIENT_PAY_BANK = "client:pay:bank"               # :<bank_id>
    CLIENT_PAY_SBP = "client:pay:sbp"
    CLIENT_PAYMENT_DONE = "client:payment:done"
    CLIENT_PAYMENT_CANCEL = "client:payment:cancel"

    # =====================================================
    # OPERATOR
    # =====================================================
    OP_ALIVE = "operator:alive"
    OP_SHIFT_START = "operator:shift:start"
    OP_SHIFT_CONFIRM = "operator:shift:confirm"
    OP_SHIFT_CANCEL = "operator:shift:cancel"
    OP_SHIFT_STOP = "operator:shift:stop"
    OP_SHIFT_EDIT_ADDRESS = "operator:shift:edit_address"

    OP_ORDER_ACCEPT = "operator:order:accept"         # :<order_id>
    OP_ORDER_READY = "operator:order:ready"           # :<order_id>
    OP_ORDER_SENT = "operator:order:sent"             # :<order_id>

    # =====================================================
    # ADMIN
    # =====================================================
    ADMIN_PRODUCTS = "admin:products"
    ADMIN_WAREHOUSES = "admin:warehouses"
    ADMIN_OPERATORS = "admin:operators"
