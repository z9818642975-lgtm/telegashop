class CB:
    # =====================================================
    # UNIVERSAL BACK (single source of truth)
    # =====================================================
    BACK = "back"

    # -------- backward compatibility --------
    BACK_MENU = BACK
    BACK_CATALOG = BACK
    BACK_CART = BACK
    BACK_CHECKOUT = BACK
    BACK_PROFILE = BACK
    BACK_ADMIN = BACK
    BACK_OPERATOR = BACK

    # =====================================================
    # CART
    # =====================================================
    CART_OPEN = "cart:open"
    CART_CLEAR = "cart:clear"
    CART_CHECKOUT = "cart:checkout"

    # legacy aliases
    CART = CART_OPEN
    OPEN_CART = CART_OPEN

    # =====================================================
    # CHECKOUT
    # =====================================================
    CHECKOUT_OPEN = "checkout:open"
    CHECKOUT_PAY = "checkout:pay"
    CHECKOUT_CANCEL = "checkout:cancel"

    # =====================================================
    # PAYMENT (LEGACY + CURRENT)
    # =====================================================
    PAYMENT = "payment:open"
    PAYMENT_CASH = "payment:cash"
    PAYMENT_CARD = "payment:card"

    # legacy aliases
    PAY_CASH = PAYMENT_CASH
    PAY_CARD = PAYMENT_CARD

    # =====================================================
    # OPERATOR
    # =====================================================
    OP_PANEL = "operator:panel"
    OP_ORDERS = "operator:orders"
    OP_ORDERS_PAGE = "operator:orders:page:"

    # =====================================================
    # ADMIN
    # =====================================================
    ADMIN_PANEL = "admin:panel"
    ADMIN_OPERATORS = "admin:operators"
    ADMIN_OPERATOR_ADD = "admin:operator:add"
    ADMIN_OPERATOR_ARCHIVE = "admin:operator:archive:"
    ADMIN_SALARY = "admin:salary"
    ADMIN_SLA = "admin:sla"

    # =====================================================
    # REPORTS
    # =====================================================
    REPORTS_MENU = "reports:menu"
    REPORTS_BY_OPERATOR = "reports:operator"
    REPORTS_EXPORT_CSV = "reports:export:csv"
    REPORTS_EXPORT_PDF = "reports:export:pdf"

