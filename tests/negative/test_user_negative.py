import allure
import pytest


@allure.epic("Pet Store API")
@allure.feature("User")
class TestUserClientNegative:
    def test_add_user_with_empty_payload_returns_error(self, user_client):
        add_resp = user_client.add_user({})

        assert add_resp.status_code == 405
        # Баг - респонс возварщает статус 200 а ожидаем 405

    @pytest.mark.parametrize(
        "username",
        ["non_existent_user_xyz_123", ""],
        ids=["несуществующий юзер", "пустой username"],
    )
    def test_get_non_existent_user_returns_not_found(self, user_client, username):
        """Запрос несуществующего пользователя должен вернуть 404."""
        resp = user_client.get_user(username)

        assert resp.status_code == 404

    def test_delete_non_existent_user_returns_error(self, user_client):
        """Удаление несуществующего пользователя."""
        resp = user_client.delete_user("totally_fake_user_999")

        assert resp.status_code == 404

    def test_update_non_existent_user_returns_error(self, user_client):
        """Обновление несуществующего пользователя."""
        resp = user_client.update_user("totally_fake_user_999", {"email": "x@x.com"})

        assert resp.status_code == 404

    @pytest.mark.parametrize(
        "invalid_email",
        ["not-an-email", "missing@", "@nodomain.com", ""],
        ids=["без домена", "без части после @", "без имени", "пустая строка"],
    )
    def test_add_user_with_invalid_email(
        self, user_client, user_factory, invalid_email
    ):
        """Невалидный email должен возвращать ошибку валидации."""
        payload = user_factory(email=invalid_email)

        resp = user_client.add_user(payload)

        # 400 = Bad Request (невалидные данные)
        assert resp.status_code == 400
