
from prometheus_client import Counter
ORDERS_CREATED = Counter("orders_created_total", "Total orders created")
PAYMENTS_CONFIRMED = Counter("payments_confirmed_total", "Total payments confirmed")
ADMIN_CALLS = Counter("admin_calls_total", "Admin calls in chat")
ORDERS_DONE = Counter("orders_done_total", "Total orders done")
