import os

from sqlalchemy import text
from sqlmodel import Session

from app.core.settings import get_settings


def test_healthcheck(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_connection(session: Session):
    result = session.execute(text("SELECT 1")).scalar_one()

    assert result == 1


def test_database_connection_target(session: Session):
    settings = get_settings()
    postgres_db = os.environ.get("POSTGRES_DB")

    result = session.execute(text("SELECT current_database()")).scalar_one()

    assert settings.POSTGRES_DB == postgres_db
    assert result == settings.POSTGRES_DB
