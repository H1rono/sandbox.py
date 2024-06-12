from aiohttp import web


async def ping(_handle: web.Request) -> web.Response:
    return web.Response(text="pong")


def serve() -> None:
    app = web.Application()
    app.add_routes([web.get("/ping", ping)])
    web.run_app(app)
