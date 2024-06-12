from aiohttp import web


# GET /ping
async def ping(_handle: web.Request) -> web.Response:
    return web.Response(text="pong")


# GET /hello/{name}
async def hello(req: web.Request) -> web.Response:
    name = req.match_info.get("name")
    return web.Response(text=f"Hello, {name}!")


def serve() -> None:
    app = web.Application()
    app.add_routes([web.get("/ping", ping), web.get("/hello/{name}", hello)])
    web.run_app(app)
