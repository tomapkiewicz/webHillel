from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ValidationError

User = get_user_model()


class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(
            request, username=username, password=password, **kwargs
        )
        if user and not user.profile.email_verificado:
            raise ValidationError(
                "Tu email no ha sido verificado. Por favor, verifica tu correo antes de ingresar."
            )
        elif not user:
            raise ValidationError(
                "Dirección de mail o contraseña incorrectos, probá de nuevo."
            )
        return user
