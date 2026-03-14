from typing import Any

from api.api_client import BaseApiClient


class PetApiClient(BaseApiClient):
    PET_PATH = "/pet"

    def add_pet(self, payload: dict[str, Any]):
        return self.post(self.PET_PATH, json=payload)

    def get_pet(self, pet_id: int):
        return self.get(f"{self.PET_PATH}/{pet_id}")

    def update_pet(self, payload: dict[str, Any]):
        return self.put(self.PET_PATH, json=payload)

    def delete_pet(self, pet_id: int):
        return self.delete(f"{self.PET_PATH}/{pet_id}")
