import os
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text

from alembic import command
from app.main import create_app


@pytest.mark.integration
def test_baseline_upgrade_downgrade_and_database_readiness(monkeypatch: pytest.MonkeyPatch) -> None:
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to a dedicated empty PostgreSQL database")
    monkeypatch.setenv("DATABASE_URL", url)
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    engine = create_engine(url)
    try:
        assert inspect(engine).get_table_names() == [], "Test database must be empty"
        command.upgrade(config, "head")
        command.check(config)
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
        assert inspect(engine).get_table_names() == ["alembic_version"]
        with TestClient(create_app()) as client:
            assert client.get("/api/health/ready").status_code == 200
        command.downgrade(config, "base")
        with engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM alembic_version")) == 0
        command.upgrade(config, "head")
    finally:
        engine.dispose()
