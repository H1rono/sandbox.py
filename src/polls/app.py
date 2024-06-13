from pathlib import Path
from typing import Any

import yaml
from aiohttp import web

from . import db


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Hello, aiohttp!")


async def get_questions(request: web.Request) -> web.Response:
    async with request.app["db"].acquire() as conn:
        print(type(conn))
        cursor = await conn.execute(db.question.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return web.Response(text=str(questions))


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
    app.router.add_get("/questions", get_questions)
