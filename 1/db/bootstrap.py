# bot/db/bootstrap.py


# bot/db/bootstrap.py



from sqlalchemy.ext.asyncio import AsyncEngine


from sqlalchemy import text





async def run_bootstrap(engine: AsyncEngine) -> None:


    async with engine.begin() as conn:


        res = await conn.execute(text("SELECT to_regclass('public.users')"))


        if res.scalar_one():


            return


        with open('/app/sql/schema.sql', 'r', encoding='utf-8') as f:


            await conn.execute(text(f.read()))





