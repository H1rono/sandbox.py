from aiohttp import web
from sqlalchemy import create_engine

from . import db
from .app import get_config, load_config, pg_context, setup_routes


def init_db() -> None:
    config = get_config()
    db_url = db.DSN.format(**config["postgres"])
    engine = create_engine(db_url)
    db.create_tables(engine)
    db.create_sample_data(engine)


def main() -> None:
    app = web.Application()
    setup_routes(app)
    load_config(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)
