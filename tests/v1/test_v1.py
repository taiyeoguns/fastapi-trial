from http import HTTPStatus

import pytest

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.common.schemas import UserSchema
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
    user_schema = UserSchema(
        first_name="test", last_name="user", email="test.user@email.com"
    )
    user = await create_user(test_session, user_schema)

    response = client.get(f"{V1_ENDPOINT}/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()[0]["id"] == str(user.uuid)
    assert response.json()[0]["last_name"] == user.last_name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_user(client, test_session):
    user_schema = UserSchema(
        first_name="test", last_name="user", email="test.user@email.com"
    )
    user = await create_user(test_session, user_schema)

    response = client.get(f"{V1_ENDPOINT}/user/{user.uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()["id"] == str(user.uuid)
    assert response.json()["first_name"] == user.first_name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_create_user(client, test_session):
    payload = {
        "first_name": "test",
        "last_name": "user",
        "email": "test.user@email.com",
    }

    response = client.post(f"{V1_ENDPOINT}/users", json=payload)

    users = await get_all_users(test_session)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()
    assert len(users) == 1
