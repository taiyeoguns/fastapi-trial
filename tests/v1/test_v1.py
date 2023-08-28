from http import HTTPStatus

import pytest

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.common.models import UserCreate
from app.v1.logic import create_user, get_all_users
from tests.utilities import get_test_session

V1_ENDPOINT = "/v1"


@pytest.fixture
def dependency_overrides(application):
    application.dependency_overrides[is_valid] = lambda: None
    application.dependency_overrides[get_session] = get_test_session
    yield application.dependency_overrides
    application.dependency_overrides = {}


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_users(client, test_session):
    user_schema = UserCreate(name="testuser")
    user = await create_user(test_session, user_schema)

    response = client.get(f"{V1_ENDPOINT}/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()[0]["uuid"] == str(user.uuid)
    assert response.json()[0]["name"] == user.name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_user(client, test_session):
    user_schema = UserCreate(name="testuser")
    user = await create_user(test_session, user_schema)

    response = client.get(f"{V1_ENDPOINT}/user/{user.uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()["uuid"] == str(user.uuid)
    assert response.json()["name"] == user.name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_create_user(client, test_session):
    payload = {"name": "testuser"}

    response = client.post(f"{V1_ENDPOINT}/users", json=payload)

    users = await get_all_users(test_session)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()
    assert len(users) == 1
