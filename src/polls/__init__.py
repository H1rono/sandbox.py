from aiohttp import web

from .app import setup_routes


def main() -> None:
    app = web.Application()
    setup_routes(app)
    web.run_app(app)
