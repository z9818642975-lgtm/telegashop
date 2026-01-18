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


        Проверяет активных операторов и их смены


        (V72 — без спама, только логика контроля)


        """





        operators = await self.users.get_active_operators()





        if not operators:


            return





        for op in operators:


            try:


                shift = await self.shifts.get_active(op.id)





                if not shift:


                    continue





                # ✅ здесь дальше будет SLA / авто-уведомления


                logger.debug(


                    "🟢 Operator online: tg_id=%s shift_id=%s",


                    op.tg_id,


                    shift.id,


                )





            except Exception as e:


                logger.exception(


                    "❌ Error while checking operator tg_id=%s: %s",


                    op.tg_id,


                    e,


                )





