# -*- coding: utf-8 -*-
# bot/web/health.py
# bot/web/health.py


from aiohttp import web


import asyncio


import logging





logger = logging.getLogger(__name__)





_runner = None  # Р В·Р В°РЎвЂ°Р С‘РЎвЂљР В° Р С•РЎвЂљ Р С—Р С•Р Р†РЎвЂљР С•РЎР‚Р Р…Р С•Р С–Р С• РЎРѓРЎвЂљР В°РЎР‚РЎвЂљР В°








async def run_health_server(port: int) -> None:


    global _runner





    if _runner is not None:


        logger.warning("СЂСџС™вЂ Health server already running, skip")


        return





    app = web.Application()





    async def health(request):


        return web.json_response({"status": "ok"})





    app.router.add_get("/health", health)





    runner = web.AppRunner(app)


    await runner.setup()





    site = web.TCPSite(runner, "0.0.0.0", port)


    await site.start()





    _runner = runner


    logger.info("СЂСџС™вЂ Health server started on port %s", port)





    # Р Т‘Р ВµРЎР‚Р В¶Р С‘Р С РЎвЂљР В°РЎРѓР С”РЎС“ Р В¶Р С‘Р Р†Р С•Р в„–


    while True:


        await asyncio.sleep(3600)





