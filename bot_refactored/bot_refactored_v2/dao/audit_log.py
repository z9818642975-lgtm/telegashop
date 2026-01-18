from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.models.audit_log import AuditLog

class AuditLogDAO:
    @staticmethod
    async def write(
        session: AsyncSession,
        *,
        actor_id: int | None,
        action: str,
        entity: str,
        entity_id: int | None,
    ):
        session.add(
            AuditLog(
                actor_id=actor_id,
                action=action,
                entity=entity,
                entity_id=entity_id,
            )
        )

