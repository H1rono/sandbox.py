from aiohttp import web

from .app import load_config, setup_routes


def main() -> None:
    app = web.Application()
    setup_routes(app)
    load_config(app)
    web.run_app(app)
