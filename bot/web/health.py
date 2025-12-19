from aiohttp import web
async def health(request):
    return web.json_response({"status":"ok"})
async def run_health_server(port: int):
    app = web.Application()
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    return runner
