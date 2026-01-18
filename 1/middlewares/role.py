# bot/middlewares/role.py
from aiogram import BaseMiddleware


class RoleMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # РІвЂєвЂќ Р СњР ВР С™Р С’Р С™Р С›Р в„ў Р вЂР вЂќ
        # РІвЂєвЂќ Р СњР ВР С™Р С’Р С™Р ВР Тђ DAO
        # РІвЂєвЂќ Р СњР ВР С™Р С’Р С™Р С›Р вЂњР С› create/get
        # user Р С–Р В°РЎР‚Р В°Р Р…РЎвЂљР С‘РЎР‚Р С•Р Р†Р В°Р Р… EnsureUserMiddleware
        return await handler(event, data)

