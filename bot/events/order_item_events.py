# bot/events/order_item_events.py
from dataclasses import dataclass

# bot/events/order_item_events.py
from bot.models.enums import OrderItemStatus


@dataclass(slots=True)


class OrderItemStatusChanged:


    client_id: int


    order_item_id: int


    product_title: str


    status: OrderItemStatus







