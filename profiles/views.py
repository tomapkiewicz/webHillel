from django.shortcuts import render
from registration.models import Profile
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


# Create your views here.
class ProfileList(ListView):
    model = Profile
    template_name = "profiles/profile_list.html"
    paginate_by = 0
    is_paginated = False


class ProfileDetail(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_object(self):
        return get_object_or_404(Profile,
                                 user__username=self.kwargs['username'])
