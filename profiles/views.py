from django.http import JsonResponse
from registration.models import Profile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # ✅ Import Q for advanced filtering
from django.shortcuts import get_object_or_404 

@method_decorator(login_required, name="dispatch")
class ProfileList(ListView):
    model = Profile
    template_name = "profiles/profile_list.html"
    paginate_by = 20

    def get_queryset(self):
        """Retrieve profiles, filtering by search query if provided."""
        queryset = super().get_queryset().select_related("user").order_by("user__username")

        # Get search query from GET parameters
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            words = search_query.split()

            # If the search query has more than one word, assume full name
            if len(words) > 1:
                first_name, last_name = words[0], " ".join(words[1:])
                search_filter = Q(nombre__icontains=first_name, apellido__icontains=last_name)
            else:
                search_filter = Q()

            # Apply additional filters for username, email, and individual words
            search_filter |= (
                Q(user__username__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(nombre__icontains=search_query) |
                Q(apellido__icontains=search_query)
            )

            queryset = queryset.filter(search_filter)

        return queryset


    def render_to_response(self, context, **response_kwargs):
        """Return JSON response if AJAX request, otherwise render template."""
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            profiles = context["page_obj"]
            profile_data = [
                {"nombre": p.nombre, "apellido": p.apellido, "user": p.user.username}
                for p in profiles
            ]
            return JsonResponse({"profiles": profile_data, "has_next": profiles.has_next()})

        return super().render_to_response(context, **response_kwargs)  # ✅ Fixed the extra quote

@method_decorator(login_required, name="dispatch")
class ProfileDetail(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs["username"])
