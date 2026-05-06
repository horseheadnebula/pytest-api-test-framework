import logging

import pytest

from api.pet_api import PetApiClient
from api.user_api import UserApiClient
from config.payloads import GeneratePet, GenerateUser
from config.settings import BASE_URL


@pytest.fixture(scope="session")
def pet_client():
    pet_client = PetApiClient(BASE_URL)
    return pet_client


@pytest.fixture(scope="session")
def user_client():
    user_client = UserApiClient(BASE_URL)
    return user_client


@pytest.fixture()
def pet_factory():
    def _factory(**kwargs) -> dict:
        return GeneratePet(**kwargs).build_payload()

    return _factory


@pytest.fixture()
def created_pet(pet_client, pet_factory):
    created_pet_ids: list[int] = []

    def _factory(**kwargs) -> dict:
        pet = pet_factory(**kwargs)
        response = pet_client.add_pet(pet)
        response.raise_for_status()
        created_pet_ids.append(pet["id"])
        return pet

    yield _factory

    for pet_id in created_pet_ids:
        resp = pet_client.delete_pet(pet_id)
        if resp.status_code not in (200, 404):
            logging.warning(
                "Cleanup failed for pet_id=%s: %s", pet_id, resp.status_code
            )


@pytest.fixture()
def user_factory():
    def _factory(**kwargs) -> dict:
        return GenerateUser(**kwargs).build_payload()

    return _factory


@pytest.fixture
def created_user(user_client, user_factory):
    created_usernames: list[str] = []

    def _factory(**kwargs) -> dict:
        user = user_factory(**kwargs)
        response = user_client.add_user(user)
        response.raise_for_status()
        created_usernames.append(user["username"])
        return user

    yield _factory

    for username in created_usernames:
        resp = user_client.delete_user(username)
        if resp.status_code not in (200, 404):
            logging.warning(
                "Cleanup failed for pet_id=%s: %s", username, resp.status_code
            )
