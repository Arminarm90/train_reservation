from django.urls import path
from .views import LoginAPIView, UserRegistrationAPIView, TokenRefreshView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("register/", UserRegistrationAPIView.as_view(), name="register-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
