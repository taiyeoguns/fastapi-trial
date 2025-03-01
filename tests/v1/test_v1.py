import uuid
from http import HTTPStatus

import pytest

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.v1.logic import get_all_users

V1_ENDPOINT = "/v1"


@pytest.fixture
def dependency_overrides(application, get_test_session):
    application.dependency_overrides[is_valid] = lambda: None
    application.dependency_overrides[get_session] = get_test_session
    yield application.dependency_overrides
    application.dependency_overrides = {}


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_users_unauthorized(client):
    response = await client.get(f"{V1_ENDPOINT}/users")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_user_unauthorized(client):
    user_uuid = str(uuid.uuid4())
    response = await client.get(f"{V1_ENDPOINT}/user/{user_uuid}")
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_users(auth_client, test_user):
    response = await auth_client.get(f"{V1_ENDPOINT}/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()[0]["id"] == str(test_user.uuid)
    assert response.json()[0]["last_name"] == test_user.last_name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_user(auth_client, test_user):
    response = await auth_client.get(f"{V1_ENDPOINT}/user/{test_user.uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()
    assert response.json()["id"] == str(test_user.uuid)
    assert response.json()["first_name"] == test_user.first_name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_unavailable_user(auth_client):
    response = await auth_client.get(f"{V1_ENDPOINT}/user/{str(uuid.uuid4())}")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_create_user(auth_client, test_session):
    payload = {
        "first_name": "sample",
        "last_name": "user",
        "email": "sample.user@email.com",
    }

    response = await auth_client.post(f"{V1_ENDPOINT}/users", json=payload)

    users = await get_all_users(test_session)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()
    assert len(users) == 2
