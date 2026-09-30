import os

from sqlalchemy import Engine, create_engine


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL must be configured")
    return url


def create_database_engine() -> Engine:
    return create_engine(
        database_url(),
        pool_pre_ping=True,
        connect_args={"connect_timeout": 3},
    )
