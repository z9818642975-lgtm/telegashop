from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.chat_sla import ChatSLA

OPERATOR_SLA = timedelta(minutes=5)
ADMIN_SLA = timedelta(minutes=10)


async def update_client_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_client_msg_at = datetime.utcnow()


async def update_operator_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_operator_msg_at = datetime.utcnow()


async def update_admin_message(session: AsyncSession, order_id: int):
    sla = await _get_or_create(session, order_id)
    sla.last_admin_msg_at = datetime.utcnow()


async def get_sla_violations(session: AsyncSession):
    now = datetime.utcnow()
    res = await session.execute(select(ChatSLA))
    slas = res.scalars().all()

    violations = []

    for sla in slas:
        if (
            sla.last_client_msg_at
            and (
                not sla.last_operator_msg_at
                or sla.last_operator_msg_at < sla.last_client_msg_at
            )
            and now - sla.last_client_msg_at > OPERATOR_SLA
        ):
            violations.append(("operator", sla.order_id))

        if (
            sla.last_operator_msg_at
            and (
                not sla.last_admin_msg_at
                or sla.last_admin_msg_at < sla.last_operator_msg_at
            )
            and now - sla.last_operator_msg_at > ADMIN_SLA
        ):
            violations.append(("admin", sla.order_id))

    return violations


async def _get_or_create(session: AsyncSession, order_id: int) -> ChatSLA:
    res = await session.execute(
        select(ChatSLA).where(ChatSLA.order_id == order_id)
    )
    sla = res.scalar_one_or_none()
    if sla:
        return sla

    sla = ChatSLA(order_id=order_id)
    session.add(sla)
    return sla

