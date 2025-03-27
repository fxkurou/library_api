from django.test import tag
from rest_framework.test import APITestCase

from api.users.factories.user_factory import UserFactory
from api.users.serializers import UserSerializer


@tag("serializers")
class UserSerializerTestCase(APITestCase):
    def test_user_serializer_successful(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["first_name"], user.first_name)
        self.assertEqual(serializer.data["last_name"], user.last_name)
        self.assertEqual(serializer.data["email"], user.email)
        self.assertEqual(serializer.data["phone"], user.phone)

    def test_user_serializer_unsuccessful(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        self.assertNotEqual(serializer.data["first_name"], f"{user.first_name} {user.first_name}")
        self.assertNotEqual(serializer.data["last_name"], f"{user.last_name} {user.last_name}")
        self.assertNotEqual(serializer.data["email"], f"{user.email} {user.email}")
        self.assertNotEqual(serializer.data["phone"], f"{user.phone} {user.phone}")

    def test_user_serializer_create(self):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@gmail.com",
            "phone": "+380123456789",
            "password": "password123",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.phone, data["phone"])
        self.assertTrue(user.check_password(data["password"]))

    def test_user_serializer_update(self):
        user = UserFactory()
        data = {
            "first_name": "New",
            "last_name": "Name",
            "email": "test@gmail.com",
            "password": "password123",
        }
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, data["first_name"])
        self.assertEqual(updated_user.last_name, data["last_name"])
        self.assertEqual(updated_user.email, data["email"])
        self.assertTrue(updated_user.check_password(data["password"]))
