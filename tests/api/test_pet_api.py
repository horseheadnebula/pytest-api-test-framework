import allure
import pytest

from models.pet_model import PetSchema


@allure.epic("Pet Store API")
@allure.feature("Pet")
class TestPetClientCrud:
    @pytest.mark.parametrize(
        "kwargs",
        [
            ({"status": "available"}),
            ({"category": {"id": 3, "name": "bird"}}),
            ({"tags": [{"id": 1, "name": "cute"}]}),
        ],
        ids=["pet w/ status", "pet w/ category", "pet w/ tags"],
    )
    def test_add_pet(self, pet_client, created_pet, kwargs):
        pet = created_pet(**kwargs)

        get_resp = pet_client.get_pet(pet["id"])

        pet_model = PetSchema.model_validate(get_resp.json())

        assert pet_model.id == pet["id"]
        assert pet_model.name == pet["name"]
        assert pet_model.status == pet["status"]

    def test_get_pet(self, pet_client, created_pet):
        pet = created_pet()

        get_resp = pet_client.get_pet(pet["id"])

        assert get_resp.status_code == 200
        assert get_resp.headers["Content-Type"] == "application/json"

    @pytest.mark.parametrize(
        "new_status", [("pending"), ("sold")], ids=["status: pending", "status: sold"]
    )
    def test_update_pet(self, pet_client, created_pet, new_status):
        pet = created_pet()

        pet["status"] = new_status
        upd_resp = pet_client.update_pet(pet)
        assert upd_resp.status_code == 200

        get_resp = pet_client.get_pet(pet["id"])

        pet_model = PetSchema.model_validate(upd_resp.json())

        assert get_resp.status_code == 200
        assert upd_resp.headers["Content-Type"] == "application/json"

        assert pet_model.id == get_resp.json()["id"]
        assert pet_model.name == get_resp.json()["name"]
        assert pet_model.status == get_resp.json()["status"]

    def test_delete_pet(self, pet_client, created_pet):
        pet = created_pet()

        del_resp = pet_client.delete_pet(pet["id"])
        assert del_resp.status_code == 200

        get_resp = pet_client.get_pet(pet["id"])
        assert get_resp.status_code == 404
        assert del_resp.headers["Content-Type"] == "application/json"
