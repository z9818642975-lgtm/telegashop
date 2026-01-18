from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.audit_log import AuditLogDAO


async def log_payment_event(
    session: AsyncSession,
    *,
    actor_id: int,
    action: str,
    order_id: int,
):
    await AuditLogDAO.write(
        session,
        actor_id=actor_id,
        action=action,
        entity="order",
        entity_id=order_id,
    )

