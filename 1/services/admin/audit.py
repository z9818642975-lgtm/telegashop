# bot/services/admin/audit.py


# bot/services/admin/audit.py



from sqlalchemy.ext.asyncio import AsyncSession


from bot.models.audit_log import AuditLog





async def audit(session: AsyncSession, actor_id: int, action: str, entity: str, entity_id: int | None = None):


    session.add(AuditLog(


        actor_id=actor_id,


        action=action,


        entity=entity,


        entity_id=entity_id


    ))


    await session.commit()





