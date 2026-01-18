import time

# client_id -> last_message_ts
_LAST_MESSAGE = {}

RATE_LIMIT_SECONDS = 10  # 1 сообщение / 10 сек


def check_client_rate_limit(client_id: int) -> bool:
    now = time.time()
    last = _LAST_MESSAGE.get(client_id)

    if last and now - last < RATE_LIMIT_SECONDS:
        return False

    _LAST_MESSAGE[client_id] = now
    return True

