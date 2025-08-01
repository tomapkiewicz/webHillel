"""webhillel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.urls import PagesPatterns
from profiles.urls import ProfilesPatterns
from django.conf import settings
from registration.views import CustomPasswordResetView   

urlpatterns = [
    path("", include("core.urls")),
    path("pages/", include(PagesPatterns)),
    path("profiles/", include(ProfilesPatterns)),
    path("admin/", admin.site.urls),
    # paths de Auth


    # 👉 Tu vista custom de reset
    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
 

    path("accounts/", include("django.contrib.auth.urls")),  # ✅ Re-add this
    path("accounts/", include("allauth.urls")),  # ✅ Keep allauth
    path("accounts/", include("registration.urls")),  # ✅ Keep registration


]

# ✅ Serve media files in DEBUG mode
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)