# bot/middlewares/shift_guard.py
# bot/services/shift_guard.py

# bot/middlewares/shift_guard.py
# bot/services/shift_guard.py





from datetime import datetime, timedelta





from sqlalchemy import select


from sqlalchemy.ext.asyncio import AsyncSession





from bot.models.operator_shift import OperatorShift


from bot.exceptions import ForbiddenError








SHIFT_TTL_MINUTES = 30








async def ensure_operator_on_shift(


    *,


    session: AsyncSession,


    operator_id: int,


) -> OperatorShift:


    """


    Р СџРЎР‚Р С•Р Р†Р ВµРЎР‚РЎРЏР ВµРЎвЂљ, РЎвЂЎРЎвЂљР С• Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р Р…Р В°РЎвЂ¦Р С•Р Т‘Р С‘РЎвЂљРЎРѓРЎРЏ Р Р…Р В° Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•Р в„– РЎРѓР СР ВµР Р…Р Вµ.





    РІСљвЂќ Р ВµРЎРѓР В»Р С‘ РЎРѓР СР ВµР Р…РЎвЂ№ Р Р…Р ВµРЎвЂљ РІвЂ вЂ™ ForbiddenError


    РІСљвЂќ Р ВµРЎРѓР В»Р С‘ РЎРѓР СР ВµР Р…Р В° Р С—РЎР‚Р С•РЎвЂљРЎС“РЎвЂ¦Р В»Р В° РІвЂ вЂ™ Р В°Р Р†РЎвЂљР С•Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР С‘Р Вµ + ForbiddenError


    РІСљвЂќ Р ВµРЎРѓР В»Р С‘ Р Р†РЎРѓРЎвЂ Р С•Р С” РІвЂ вЂ™ Р Р†Р С•Р В·Р Р†РЎР‚Р В°РЎвЂ°Р В°Р ВµРЎвЂљ OperatorShift


    """





    result = await session.execute(


        select(OperatorShift).where(


            OperatorShift.operator_id == operator_id,


            OperatorShift.ended_at.is_(None),


        )


    )


    shift = result.scalar_one_or_none()





    if not shift:


        raise ForbiddenError("РІСњРЉ Р РЋР СР ВµР Р…Р В° Р Р…Р Вµ Р Р…Р В°РЎвЂЎР В°РЎвЂљР В°")





    now = datetime.utcnow()





    if shift.started_at < now - timedelta(minutes=SHIFT_TTL_MINUTES):


        shift.ended_at = now


        await session.flush()


        raise ForbiddenError("РІРЏВ± Р РЋР СР ВµР Р…Р В° Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР В° Р С—Р С• РЎвЂљР В°Р в„–Р СР В°РЎС“РЎвЂљРЎС“")





    return shift





