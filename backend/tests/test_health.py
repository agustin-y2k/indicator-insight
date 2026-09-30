from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import create_app


def test_liveness_and_readiness() -> None:
    engine = MagicMock()
    with patch("app.main.create_database_engine", return_value=engine):
        with TestClient(create_app()) as client:
            assert client.get("/api/health/live").json() == {"status": "ok"}
            response = client.get("/api/health/ready")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
    engine.dispose.assert_called_once()


def test_database_unavailable_does_not_expose_internal_error() -> None:
    engine = MagicMock()
    engine.connect.side_effect = OperationalError("private connection details", {}, Exception())
    with patch("app.main.create_database_engine", return_value=engine):
        with TestClient(create_app()) as client:
            assert client.get("/api/health/live").status_code == 200
            response = client.get("/api/health/ready")
            assert response.status_code == 503
            assert response.json() == {"status": "unavailable"}


def test_missing_database_configuration_fails_explicitly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL must be configured"):
        with TestClient(create_app()):
            pass
