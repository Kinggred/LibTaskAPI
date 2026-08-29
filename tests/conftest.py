import subprocess
import sys
from collections.abc import Generator
from uuid import UUID, uuid4

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

load_dotenv(".env.test", override=True)

from app.core.settings import get_settings

get_settings.cache_clear()
settings = get_settings()

from app.api.main import app
from app.core.database import get_session


@pytest.fixture(scope="session", autouse=True)
def migrate_test_database():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "app/alembic.ini",
            "upgrade",
            "head",
        ],
        check=True,
    )


@pytest.fixture(name="engine", scope="session")
def engine_fixture():
    engine = create_engine(
        str(settings.POSTGRES_DSN),
        echo=False,
        pool_pre_ping=True,
    )

    yield engine

    engine.dispose()


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session]:
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient]:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def make_uuid():
    def _make_uuid() -> UUID:
        return uuid4()

    return _make_uuid
