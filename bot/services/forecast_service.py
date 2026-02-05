# bot/services/forecast_service.py
from datetime import datetime, timedelta


class ForecastService:
    @staticmethod
    def estimate_ready_at(items_count: int) -> datetime:
        minutes = max(10, items_count * 3)
        return datetime.utcnow() + timedelta(minutes=minutes)

