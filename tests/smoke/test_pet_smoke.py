import allure
import pytest


@allure.epic("Pet Store API")
@allure.feature("Pet")
@allure.story("Smoke")
class TestPetSmoke:
    def test_create_and_get_pet_is_alive(self, pet_client, created_pet):
        """Базовая проверка: можно создать питомца и получить его."""
        pet = created_pet()

        resp = pet_client.get_pet(pet["id"])

        assert resp.status_code == 200

    def test_api_returns_json(self, pet_client, created_pet):
        """Сервер отдаёт JSON, а не HTML-ошибку."""
        pet = created_pet()

        resp = pet_client.get_pet(pet["id"])

        assert "application/json" in resp.headers["Content-Type"]
