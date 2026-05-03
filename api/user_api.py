from typing import Any

from api.api_client import BaseApiClient


class UserApiClient(BaseApiClient):
    USER_PATH = "/user"

    def add_user(self, payload: dict[str, Any]):
        return self.post(self.USER_PATH, json=payload)

    def get_user(self, username: str):
        return self.get(f"{self.USER_PATH}/{username}")

    def update_user(self, username: str, payload: dict[str, Any]):
        return self.put(f"{self.USER_PATH}/{username}", json=payload)

    def delete_user(self, username: str):
        return self.delete(f"{self.USER_PATH}/{username}")
