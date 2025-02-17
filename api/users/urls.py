from django.urls import path

from api.users.views import BaserProfileObtainToken, UserDetailView, UserRegisterView

urlpatterns = [
    path("token/", BaserProfileObtainToken.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<int:pk>/", UserDetailView.as_view(), name="user"),
]
