import pytest

from api.pet_api import PetApiClient
from api.user_api import UserApiClient
from config.payloads import Category, GeneratePet, GenerateUser, Tags
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
    def _factory(
        pet_id: int | None = None,
        name: str | None = None,
        status: str | None = None,
        category: Category | None = None,
        photo_urls: list[str] | None = None,
        tags: list[Tags] | None = None,
    ) -> dict:
        return GeneratePet(
            pet_id=pet_id,
            name=name,
            status=status,
            category=category,
            photo_urls=photo_urls,
            tags=tags,
        ).build_payload()

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
        pet_client.delete_pet(pet_id)


@pytest.fixture()
def user_factory():
    def _factory(
        user_id: int | None = None,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        user_status: int | None = None,
    ) -> dict:
        return GenerateUser(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            user_status=user_status,
        ).build_payload()

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
        user_client.delete_user(username)
