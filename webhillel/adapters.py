from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")
        if not email:
            return  # No email provided, proceed as usual
        
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)  # ✅ Force link to existing user
        except User.DoesNotExist:
            pass  # If no user exists, proceed with normal signup