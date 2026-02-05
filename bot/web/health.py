# bot/web/health.py
# bot/web/health.py
# bot/web/health.py


import asyncio
import logging

from aiohttp import web

logger = logging.getLogger(__name__)





_runner = None  # защита от повторного старта








async def run_health_server(port: int) -> None:


    global _runner





    if _runner is not None:


        logger.warning("🚑 Health server already running, skip")


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


    logger.info("🚑 Health server started on port %s", port)





    # держим таску живой


    while True:


        await asyncio.sleep(3600)







