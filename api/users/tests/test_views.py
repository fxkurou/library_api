from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.users.factories.user_factory import UserFactory


@tag("views")
class UserDetailTestCase(APITestCase):
    def test_get_user_success(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["phone"], user.phone)

    def test_get_user_fail(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse("user", kwargs={"pk": user.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_user_success(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        data = {
            "first_name": "New",
            "last_name": "Name",
            "email": "test@gmail.com",
            "phone": "+380123456789",
            "password": "password123",
        }
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["phone"], data["phone"])

    def test_put_user_fail(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        data = {
            "first_name": "New",
            "last_name": "Name",
            "email": "not_email",
            "phone": "+380123456789",
        }
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_user_success(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        data = {
            "first_name": "New",
        }
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], data["first_name"])

    def test_patch_user_fail(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        data = {
            "email": "not_email",
        }
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_success(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse("user", kwargs={"pk": user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_fail(self):
        user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        url = reverse("user", kwargs={"pk": user.id + 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
