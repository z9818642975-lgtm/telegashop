import time

_last_message = {}

class AntiSpamService:
    @staticmethod
    def check(client_id: int, seconds: int = 10) -> bool:
        now = time.time()
        last = _last_message.get(client_id, 0)
        if now - last < seconds:
            return False
        _last_message[client_id] = now
        return True

