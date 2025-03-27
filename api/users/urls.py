from django.urls import path

from api.users.views import BaseTokenObtainPairView, BaserTokenRefreshView, UserDetailView, UserRegisterView

urlpatterns = [
    path("token/", BaseTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", BaserTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<int:pk>/", UserDetailView.as_view(), name="user"),
]
