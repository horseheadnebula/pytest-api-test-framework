import allure
import pytest


@allure.epic("Pet Store API")
@allure.feature("Pet")
class TestPetClientNegative:
    def test_add_pet_with_empty_payload_returns_error(self, pet_client):
        response = pet_client.add_pet({})

        assert response.status_code == 405

    @pytest.mark.parametrize(
        "pet_id",
        [0, 999999999],
        ids=["boundary id = 0", "non-existent id"],
    )
    def test_get_non_existent_pet_returns_not_found(self, pet_client, pet_id):
        response = pet_client.get_pet(pet_id)

        assert response.status_code == 404

    def test_update_pet_without_id_returns_error(self, pet_client):
        payload = {"name": "broken-pet", "photoUrls": ["https://example.com/pet.jpg"]}

        response = pet_client.update_pet(payload)

        assert response.status_code in (400, 405)

    @pytest.mark.parametrize(
        "pet_id",
        ["invalid-id", -1],
        ids=["string id", "negative id"],
    )
    def test_delete_pet_with_invalid_id_returns_error(self, pet_client, pet_id):
        response = pet_client.delete_pet(pet_id)

        assert response.status_code in (400, 404, 405)
