import allure
import pytest

from models.user_model import UserSchema


@pytest.mark.api
class TestUserClientCrud:
    def test_add_user(self, user_client, created_user):
        user = created_user()

        get_resp = user_client.get_user(user["username"])

        user_model = UserSchema.model_validate(get_resp.json())

        assert get_resp.status_code == 200, get_resp.json()
        assert user_model.username == user["username"]
        assert user_model.id == user["id"]
        assert user_model.email == user["email"]

    def test_get_user(self, user_client, created_user):
        user = created_user()

        get_resp = user_client.get_user(user["username"])

        user_model = UserSchema.model_validate(get_resp.json())

        assert get_resp.status_code == 200, get_resp.json()
        assert user_model.username == user["username"]

    @pytest.mark.parametrize("new_email", [({"email": "new@email.com"})])
    def test_update_user(self, user_client, created_user, new_email):
        user = created_user()

        update_resp = user_client.update_user(user["username"], {**user, **new_email})
        updated_user_resp = user_client.get_user(user["username"])

        user_model = UserSchema.model_validate(updated_user_resp.json())

        assert update_resp.status_code == 200, update_resp.json()
        assert user_model.email == new_email["email"]

    def test_delete_user(self, user_client, created_user):
        user = created_user()

        delete_resp = user_client.delete_user(user["username"])
        get_resp = user_client.get_user(user["username"])

        assert delete_resp.status_code == 200, delete_resp.json()
        assert get_resp.status_code == 404

    @pytest.mark.parametrize(
        "update_data",
        [
            {"firstName": "NewName"},
            {"lastName": "NewLastName"},
            {"phone": "123-456-7890"},
        ],
        ids=["update name", "update lastname", "update phone"],
    )
    def test_update_user_different_fields(self, user_client, created_user, update_data):
        """Можно обновлять разные поля пользователя."""
        user = created_user()

        resp = user_client.update_user(user["username"], update_data)

        assert resp.status_code == 200
