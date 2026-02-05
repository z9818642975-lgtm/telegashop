# bot/services/admin/sla.py


# bot/services/admin/sla.py



from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def operator_sla(session: AsyncSession):


    q = await session.execute(text("""


        SELECT operator_id,


               AVG(EXTRACT(EPOCH FROM (closed_at - created_at))) AS avg_sla,


               PERCENTILE_CONT(0.5)


               WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (closed_at - created_at))) AS median_sla


        FROM orders


        WHERE status='DONE' AND operator_id IS NOT NULL


        GROUP BY operator_id


    """))


    return q.all()






