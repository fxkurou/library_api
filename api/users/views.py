from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.models import User
from api.users.serializers import BaseTokenObtainPairSerializer, UserDetailSerializer, UserRegisterSerializer


class BaserProfileObtainToken(TokenObtainPairView):
    """
    Custom token obtain view with user profile data.
    This view is used to obtain a JWT token for a user.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = BaseTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    Custom user registration view.
    This view is used to register a new user.
    The user profile data is returned in the response.
    The user profile data includes the user's first name, last name, email, and phone number.
    """

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserDetailView(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    Custom user detail view.
    This view is used to retrieve and update a user's profile.
    The user profile data is returned in the response.
    The user profile data includes the user's first name, last name, email, phone number and favorite_categories.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        return obj

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
