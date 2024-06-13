from aiohttp import web


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Hello, aiohttp!")


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
