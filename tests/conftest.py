import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.main import create_app
from app.common.database import Base
from app.common.factories import UserFactory
from config import TESTING_CONFIG


@pytest.fixture(name="application")
def fixture_application():
    """Fixture to set up application with configuration

    Returns:
        application -- Application context
    """
    yield create_app()


@pytest.fixture(name="test_engine")
def fixture_test_engine():
    yield create_async_engine(TESTING_CONFIG.DATABASE_URL)


@pytest_asyncio.fixture(name="create_tables")
async def fixture_create_tables(test_engine):
    async def inner():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    return inner


@pytest_asyncio.fixture(name="test_user")
async def fixture_test_user(test_session):
    yield await test_session.run_sync(
        UserFactory.create_instance,
        first_name="Test",
        last_name="User",
        api_key="00000000-0000-0000-0000-000000000000",
    )


@pytest_asyncio.fixture(name="client")
async def fixture_client(application):
    """Fixture for HTTP test client using httpx.AsyncClient

    Arguments:
        application -- Application context

    Returns:
        client -- HTTP async client
    """
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(name="auth_client")
async def fixture_auth_client(client, test_user):
    client.headers.update({"X-Api-Key": str(test_user.api_key)})
    yield client


@pytest_asyncio.fixture(name="test_session")
async def fixture_test_session(test_engine, create_tables):
    SessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, expire_on_commit=False, bind=test_engine
    )
    async with SessionLocal() as session:
        await create_tables()
        yield session


@pytest_asyncio.fixture(name="get_test_session")
async def fixture_get_test_session(test_session):
    async def inner():
        return test_session

    return inner
