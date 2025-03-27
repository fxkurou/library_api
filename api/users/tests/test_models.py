from django.test import tag
from rest_framework.test import APITestCase

from api.users.factories.user_factory import UserFactory


@tag("models")
class UserTestCase(APITestCase):
    def test_user_model_successful(self):
        user = UserFactory(
            first_name="First Name 0",
            last_name="Last Name 0",
            email="test@gmail.com",
            phone="+380501111111",
        )
        self.assertEqual(user.first_name, "First Name 0")
        self.assertEqual(user.last_name, "Last Name 0")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.phone, "+380501111111")
        self.assertEqual(user.__str__(), "First Name 0 Last Name 0")
