# bot/services/operator_sla_service.py
from datetime import datetime, timedelta


class OperatorSLAService:
    MAX_ACCEPT_DELAY = timedelta(minutes=5)

    @staticmethod
    def is_late(accepted_at: datetime, now: datetime | None = None) -> bool:
        now = now or datetime.utcnow()
        return now - accepted_at > OperatorSLAService.MAX_ACCEPT_DELAY


