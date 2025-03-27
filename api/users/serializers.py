from rest_framework import serializers

from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Base user serializer.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def create(self, validated_data):
        """
        Create a new user.

        :param validated_data: dictionary containing user data.
        :return: created user object.
        """
        email = validated_data.get("email", None)
        user = User.objects.create(username=email, **validated_data)
        user.set_password(validated_data["password"])
        return user

    def update(self, instance, validated_data):
        """
        Update a user.

        :param instance: instance of the user object.
        :param validated_data: dictionary containing user data.
        :return: updated user object.
        """
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)
