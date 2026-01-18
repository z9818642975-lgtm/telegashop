# bot/db/session.py

# bot/db/session.py
# bot/db/session.py


from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


from bot.db.engine import engine





async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(


    bind=engine,


    expire_on_commit=False,


)




