import unittest
from unittest.mock import patch
from services import user_service
from data.models import User, Role


class TestUserAuth(unittest.TestCase):

    @patch("services.user_service.read_query")
    def test_is_authenticated_valid_token(self, mock_read):
        mock_read.return_value = [(1,)]

        token = "1;testuser"

        result = user_service.is_authenticated(token)

        self.assertTrue(result)

    @patch("services.user_service.read_query")
    def test_is_authenticated_invalid_token(self, mock_read):
        mock_read.return_value = []

        token = "1;testuser"

        result = user_service.is_authenticated(token)

        self.assertFalse(result)

    @patch("services.user_service.find_by_username")
    def test_try_login_success(self, mock_find):
        mock_find.return_value = User(
            id=1,
            username="test",
            password="1234",
            role=Role.USER
        )

        user = user_service.try_login("test", "1234")

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test")

    @patch("services.user_service.find_by_username")
    def test_try_login_fail(self, mock_find):
        mock_find.return_value = None

        user = user_service.try_login("test", "1234")

        self.assertIsNone(user)

    def test_create_token(self):
        user = User(
            id=5,
            username="john",
            password="",
            role=Role.USER
        )

        token = user_service.create_token(user)

        self.assertEqual(token, "5;john")