# bot/services/salary_service.py
from bot.services.salary import calculate_salary


def process_salary(orders_count: int, rate: int) -> int:
    return calculate_salary(orders_count, rate)


