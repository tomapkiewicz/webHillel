from .forms import (
    UserCreationFormWithEmail,
    ProfileForm,
    EmailForm,
)
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from .utils import send_email_token
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .backends import EmailVerifiedBackend

User = get_user_model()

from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = 'www.hillelargentina.org.ar'
        context['protocol'] = 'https'
        print("👉 CustomPasswordResetView ejecutada correctamente")
        return context
    
    
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_backend = EmailVerifiedBackend


class VerifyEmailView(View):
    def get(self, request, pk, email):
        try:
            user = User.objects.get(pk=pk, email=email)
            user.is_active = True  # Set the user as active (verified)
            user.save()

            user.profile.email_verificado = True
            user.profile.save()
            login(request, user)  # Log in the user
            messages.success(
                request, "Tu email ha sido verificado, ya puedes ingresar."
            )
            logout(request)
        except User.DoesNotExist:
            messages.error(
                request,
                "El enlace de verificación no es válido. Por favor, intenta nuevamente.",
            )
        return redirect(
            reverse_lazy("login") + "?register"
        )  # Redirect to the login page with the query parameter


class RegisterSuccess(TemplateView):
    template_name = "registration/register_success.html"


class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse_lazy("register_success")

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        form.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control mb-2", "placeholder": "Direccion email"}
        )
        form.fields["email"].widget = forms.EmailInput(
            attrs={
                "class": "form-control mb-2",
                "placeholder": "Reingresar direccion email",
            }
        )
        form.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control mb-2", "placeholder": "Contraseña"}
        )
        form.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control mb-2", "placeholder": "Repetí la contraseña"}
        )

        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        # Send email verification link
        send_email_token(user.email, user.pk)

        return response


@method_decorator(login_required, name="dispatch")
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    # success_url = reverse_lazy('profile')
    # template_name = 'registration/profile_form.html'
    template_name_suffix = "_form"

    def get_success_url(self):
        if "completar" in self.request.GET:
            return (
                reverse_lazy("pages:page", args=[self.request.GET["pk"]])
                + "?perfilcompleto"
            )
        return reverse_lazy("profile") + "?ok"

    def get_object(self):
        # Recupera el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name="dispatch")
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy("profile")
    template_name = "registration/profile_email_form.html"

    def get_object(self):
        # Recupera el objeto que se va a editar
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields["email"].widget = forms.EmailInput(
            attrs={"class": "form-control mb-2", "placeholder": "Email"}
        )
        return form

