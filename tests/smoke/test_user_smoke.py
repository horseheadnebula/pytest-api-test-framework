class TestUserSmoke:
    def test_create_and_get_user_is_alive(self, user_client, created_user):
        user = created_user()

        resp = user_client.get_user(user["username"])

        assert resp.status_code == 200
