from sqlalchemy import Column, Date, Engine, ForeignKey, Integer, MetaData, String, Table

meta = MetaData()

question = Table(
    "question",
    meta,
    Column("id", Integer, primary_key=True),
    Column("question_text", String(200), nullable=False),
    Column("pub_date", Date, nullable=False),
)

choice = Table(
    "choice",
    meta,
    Column("id", Integer, primary_key=True),
    Column("choice_text", String(200), nullable=False),
    Column("votes", Integer, server_default="0", nullable=False),
    Column("question_id", Integer, ForeignKey("question.id", ondelete="CASCADE")),
)

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine: Engine) -> None:
    meta = MetaData()
    meta.create_all(bind=engine, tables=[question, choice])


def create_sample_data(engine: Engine) -> None:
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
