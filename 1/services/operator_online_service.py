# bot/services/operator_online_service.py
# ============================================================

# bot/services/operator_online_service.py
# ============================================================


# bot/services/operator_online_service.py


# ============================================================





from bot.dao.shifts_dao import OperatorShiftDAO


from bot.dao.users_dao import UsersDAO


from bot.core.logger import logger








class OperatorOnlineService:


    def __init__(self, session):


        self.session = session


        self.shifts = OperatorShiftDAO(session)


        self.users = UsersDAO(session)





    async def run(self, bot):


        """


        Р СџРЎР‚Р С•Р Р†Р ВµРЎР‚РЎРЏР ВµРЎвЂљ Р В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№РЎвЂ¦ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р С•Р Р† Р С‘ Р С‘РЎвЂ¦ РЎРѓР СР ВµР Р…РЎвЂ№


        (V72 РІР‚вЂќ Р В±Р ВµР В· РЎРѓР С—Р В°Р СР В°, РЎвЂљР С•Р В»РЎРЉР С”Р С• Р В»Р С•Р С–Р С‘Р С”Р В° Р С”Р С•Р Р…РЎвЂљРЎР‚Р С•Р В»РЎРЏ)


        """





        operators = await self.users.get_active_operators()





        if not operators:


            return





        for op in operators:


            try:


                shift = await self.shifts.get_active(op.id)





                if not shift:


                    continue





                # РІСљвЂ¦ Р В·Р Т‘Р ВµРЎРѓРЎРЉ Р Т‘Р В°Р В»РЎРЉРЎв‚¬Р Вµ Р В±РЎС“Р Т‘Р ВµРЎвЂљ SLA / Р В°Р Р†РЎвЂљР С•-РЎС“Р Р†Р ВµР Т‘Р С•Р СР В»Р ВµР Р…Р С‘РЎРЏ


                logger.debug(


                    "СЂСџСџСћ Operator online: tg_id=%s shift_id=%s",


                    op.tg_id,


                    shift.id,


                )





            except Exception as e:


                logger.exception(


                    "РІСњРЉ Error while checking operator tg_id=%s: %s",


                    op.tg_id,


                    e,


                )





