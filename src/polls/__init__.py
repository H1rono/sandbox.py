from aiohttp import web


def main() -> None:
    app = web.Application()
    web.run_app(app)
