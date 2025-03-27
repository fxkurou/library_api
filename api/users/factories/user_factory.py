import factory

from api.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating User objects
    """

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    password = factory.PostGenerationMethodCall("set_password", "password")
