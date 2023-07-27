from django.urls import path
from .views import ProfileDetail, ProfileList

ProfilesPatterns = (
    [
        path("", ProfileList.as_view(), name="list"),
        path("<username>/", ProfileDetail.as_view(), name="detail"),
    ],
    "profiles",
)
