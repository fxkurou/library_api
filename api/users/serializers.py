from typing import Any, Dict

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.users.models import User


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes user email in the response.
    """

    @classmethod
    def get_token(cls, user: User) -> Token:
        """
        Add user email to the token response.
        """
        token = super(BaseTokenObtainPairSerializer, cls).get_token(user)
        token["email"] = user.email
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        Add user email to the response.
        """
        data = super().validate(attrs)
        data["email"] = self.user.email
        return data


class UserBaseSerializer(serializers.ModelSerializer):
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
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
        ]


class UserRegisterSerializer(UserBaseSerializer):
    """
    User serializer for registration.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserBaseSerializer.Meta.model
        fields = UserBaseSerializer.Meta.fields + ["password"]

    def create(self, validated_data):
        """
        Create user.
        """
        email = validated_data.get("email")
        user = UserBaseSerializer.Meta.model.objects.create(username=email, **validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserDetailSerializer(UserBaseSerializer):
    """
    User detail serializer.
    """

    class Meta:
        model = UserBaseSerializer.Meta.model
        fields = UserBaseSerializer.Meta.fields

    def update(self, instance, validated_data):
        """
        Update user.
        """

        return super().update(instance, validated_data)
