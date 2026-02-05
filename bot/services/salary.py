# bot/services/salary.py
def calculate_salary(completed_orders: int, rate_per_order: int, penalties: int = 0) -> int:
    return max(0, completed_orders * rate_per_order - penalties)


