# bot/services/order_item_status.py
# bot/services/order_item_status.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.events.order_item_events import OrderItemStatusChanged
from bot.models import Order, OrderItem
from bot.models.enums import OrderItemStatus, OrderStatus


class OrderItemStatusService:


    def __init__(self, session: AsyncSession, event_bus):


        self.session = session


        self.event_bus = event_bus





    async def set_status(


        self,


        *,


        item_id: int,


        new_status: OrderItemStatus,


        actor_id: int | None = None,


    ) -> None:


        item = await self.session.scalar(


            select(OrderItem)


            .where(OrderItem.id == item_id)


            .options(


                selectinload(OrderItem.order),


                selectinload(OrderItem.product),


            )


        )


        if not item:


            raise ValueError("OrderItem not found")





        self._validate_transition(item.status, new_status)





        item.status = new_status


        item.order.status = self._aggregate_order_status(item.order)





        await self.session.commit()





        await self.event_bus.publish(


            OrderItemStatusChanged(


                client_id=item.order.client_id,


                order_item_id=item.id,


                product_title=item.product.title,


                status=new_status,


            )


        )





    # -------------------------------------------------





    def _validate_transition(self, old, new):


        allowed = {


            OrderItemStatus.NEW: {


                OrderItemStatus.ACCEPTED,


                OrderItemStatus.WAIT_PAYMENT,


            },


            OrderItemStatus.ACCEPTED: {


                OrderItemStatus.PAID,


            },


            OrderItemStatus.PAID: {


                OrderItemStatus.IN_PROGRESS,


                OrderItemStatus.READY,


            },


            OrderItemStatus.READY: {


                OrderItemStatus.DONE,


                OrderItemStatus.IN_PROGRESS,


            },


            OrderItemStatus.IN_PROGRESS: {


                OrderItemStatus.DONE,


            },


        }





        if new not in allowed.get(old, set()):


            raise ValueError(f"Invalid transition {old} → {new}")





    # -------------------------------------------------





    def _aggregate_order_status(self, order: Order) -> OrderStatus:


        statuses = {item.status for item in order.items}





        if all(s == OrderItemStatus.DONE for s in statuses):


            return OrderStatus.DONE





        if OrderItemStatus.READY in statuses:


            return OrderStatus.WAIT_OPERATOR





        if OrderItemStatus.IN_PROGRESS in statuses:


            return OrderStatus.IN_PROGRESS





        if OrderItemStatus.PAID in statuses:


            return OrderStatus.PAID





        return OrderStatus.NEW







