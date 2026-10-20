import asyncio

import httpx
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import health as health_routes
from app.core.config import get_settings
from app.db.session import get_engine
from app.main import app


def request_get(path: str) -> httpx.Response:
    async def send_request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            return await client.get(path)

    return asyncio.run(send_request())


def test_health_returns_api_status() -> None:
    response = request_get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_reports_reachable_database(
    monkeypatch,
) -> None:
    engine = create_engine("sqlite+pysqlite://")
    monkeypatch.setattr(health_routes, "get_engine", lambda: engine)

    response = request_get("/health/db")

    engine.dispose()
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "reachable"}


def test_database_health_returns_503_when_query_fails(
    monkeypatch,
) -> None:
    engine = create_engine("sqlite+pysqlite://")

    @event.listens_for(engine, "before_cursor_execute")
    def fail_query(*args, **kwargs) -> None:
        raise SQLAlchemyError("simulated database failure")

    monkeypatch.setattr(health_routes, "get_engine", lambda: engine)

    response = request_get("/health/db")

    engine.dispose()
    assert response.status_code == 503
    assert response.json() == {
        "detail": {"status": "unhealthy", "database": "unavailable"}
    }
    assert "simulated database failure" not in response.text


def test_database_health_returns_503_when_database_url_is_missing(
    monkeypatch,
) -> None:
    def fail_configuration():
        raise health_routes.DatabaseConfigurationError(
            "DATABASE_URL is not configured."
        )

    monkeypatch.setattr(health_routes, "get_engine", fail_configuration)

    response = request_get("/health/db")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {"status": "unhealthy", "database": "unavailable"}
    }


def test_engine_uses_configured_url_without_connecting(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://test_user:not-a-secret@postgres:5432/test_db",
    )
    get_settings.cache_clear()
    get_engine.cache_clear()

    engine = get_engine()
    try:
        assert engine.url.drivername == "postgresql+psycopg"
        assert engine.url.host == "postgres"
        assert engine.url.port == 5432
    finally:
        engine.dispose()
        get_engine.cache_clear()
        get_settings.cache_clear()
