from django.urls import path
from .views import HomePageView, SamplePageView, export_csv, enviar_mail

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]
