import pytest

from api.pet_api import PetApiClient
from config.payloads import Category, GeneratePet, Tags
from config.settings import BASE_URL


@pytest.fixture(scope="session")
def pet_client():
    pet_client = PetApiClient(BASE_URL)
    return pet_client


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
