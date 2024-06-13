from collections.abc import Mapping
from typing import AsyncIterator

import aiopg.sa
import sqlalchemy as sa
from aiohttp import web

meta = sa.MetaData()

question = sa.Table(
    "question",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("question_text", sa.String(200), nullable=False),
    sa.Column("pub_date", sa.Date, nullable=False),
)

choice = sa.Table(
    "choice",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("choice_text", sa.String(200), nullable=False),
    sa.Column("votes", sa.Integer, server_default="0", nullable=False),
    sa.Column("question_id", sa.Integer, sa.ForeignKey("question.id", ondelete="CASCADE")),
)

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine: sa.Engine) -> None:
    meta = sa.MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def create_sample_data(engine: sa.Engine) -> None:
    conn = engine.connect()
    conn.execute(question.insert(), [{"question_text": "What's new?", "pub_date": "2024-06-13 00:00:00+09"}])
    conn.execute(
        choice.insert(),
        [
            {"choice_text": "Not much", "votes": 0, "question_id": 1},
            {"choice_text": "The sky", "votes": 0, "question_id": 1},
            {"choice_text": "Just hacking again", "votes": 0, "question_id": 1},
        ],
    )
    conn.close()


async def pg_context(app: web.Application) -> AsyncIterator[None]:
    conf = app["config"]["postgres"]
    assert isinstance(conf, Mapping)
    engine = await aiopg.sa.create_engine(**conf)
    app["db"] = engine
    yield
    app["db"].close()
    await app["db"].wait_closed()
