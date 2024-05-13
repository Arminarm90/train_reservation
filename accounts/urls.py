from django.urls import path
from .views import (
    LoginAPIView,
    UserRegistrationAPIView,
    TokenRefreshView,
    UserDetailsAPIView,
    Changepaswword,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("register/", UserRegistrationAPIView.as_view(), name="register-login"),
    path("profile/", UserDetailsAPIView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # change password
    path("change-password/", Changepaswword.as_view(), name="change-password"),
    
]
