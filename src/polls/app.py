from pathlib import Path
from typing import Any

import yaml
from aiohttp import web


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Hello, aiohttp!")


def get_config(path: str | None = None) -> Any:
    path = path or str(Path(__file__).parent / "config.yml")
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


def load_config(app: web.Application, path: str | None = None) -> None:
    config = get_config(path)
    app["config"] = config


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
