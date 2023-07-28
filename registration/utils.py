from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.urls import reverse


def send_email_token(email, user_id):
    try:
        current_site = Site.objects.get_current()
        domain = current_site.domain if current_site else settings.ALLOWED_HOSTS[0]
        verification_url = reverse("verify_email", args=[user_id, email])
        verification_url = f"{current_site.domain}{verification_url}"
        subject = "Verificación de email"
        message = f"Haz click en el siguiente link para verificar tu correo: {verification_url}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        print("Verification URL:", verification_url)
    except Exception as e:
        print(e)
        return False
    return True
