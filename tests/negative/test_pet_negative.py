import allure
import pytest


@allure.epic("Pet Store API")
@allure.feature("Pet")
@pytest.mark.negative
class TestPetClientNegative:
    @pytest.mark.xfail(
        reason="Petstore не валидирует входные данные, баг на стороне API",
        strict=True,  # если вдруг починят — тест станет красным
    )
    def test_add_pet_with_empty_payload_returns_error(self, pet_client):
        add_resp = pet_client.add_pet({})

        assert add_resp.status_code == 405

    @pytest.mark.parametrize(
        "pet_id",
        [0, 999999999],
        ids=["boundary id = 0", "non-existent id"],
    )
    def test_get_non_existent_pet_returns_not_found(self, pet_client, pet_id):
        get_resp = pet_client.get_pet(pet_id)

        assert get_resp.status_code == 404

    @pytest.mark.xfail(
        reason="Petstore не валидирует входные данные, баг на стороне API",
        strict=True,
    )
    def test_update_pet_without_id_returns_error(self, pet_client):
        payload = {"name": "broken-pet", "photoUrls": ["https://example.com/pet.jpg"]}

        upd_resp = pet_client.update_pet(payload)

        assert upd_resp.status_code in (400, 405)

    @pytest.mark.parametrize(
        "pet_id",
        ["invalid-id", -1],
        ids=["string id", "negative id"],
    )
    def test_delete_pet_with_invalid_id_returns_error(self, pet_client, pet_id):
        del_resp = pet_client.delete_pet(pet_id)

        assert del_resp.status_code in (400, 404, 405)

    @pytest.mark.xfail(
        reason="Petstore не валидирует входные данные, баг на стороне API",
        strict=True,
    )
    def test_get_pet_with_string_id_returns_error(self, pet_client):
        """ID питомца должен быть числом, строка — ошибка."""
        resp = pet_client.get_pet("abc")

        assert resp.status_code == 400  # Bad Request

    @pytest.mark.xfail(
        reason="Petstore не валидирует входные данные, баг на стороне API",
        strict=True,
    )
    @pytest.mark.parametrize(
        "invalid_name",
        ["", "a" * 500],
        ids=["empty name", "very long name"],
    )
    def test_add_pet_with_invalid_name(self, pet_client, pet_factory, invalid_name):
        """Граничные значения для поля name."""
        payload = pet_factory(name=invalid_name)

        resp = pet_client.add_pet(payload)

        assert resp.status_code in (400, 405, 422)

    @pytest.mark.xfail(
        reason="Petstore не валидирует входные данные, баг на стороне API",
        strict=True,
    )
    def test_add_pet_with_invalid_status(self, pet_client, pet_factory):
        """Статус должен быть одним из available/pending/sold."""
        payload = pet_factory()
        payload["status"] = (
            "flying"  # подменяем после Pydantic-валидации, чтобы невалидные данные дошли до API
        )

        resp = pet_client.add_pet(payload)

        assert resp.status_code in (400, 422)
