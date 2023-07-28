from django.urls import path
from .views import (
    SignUpView,
    ProfileUpdate,
    EmailUpdate,
    RegisterSuccess,
    VerifyEmailView,
    CustomLoginView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileUpdate.as_view(), name="profile"),
    path("profile/<int>/", ProfileUpdate.as_view(), name="profile"),
    path("profile/email/", EmailUpdate.as_view(), name="profile_email"),
    path(
        "verify_email/<int:pk>/<str:email>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path("register_success", RegisterSuccess.as_view(), name="register_success"),
    path("login/", CustomLoginView.as_view(), name="login"),
]
