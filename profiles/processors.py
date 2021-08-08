from django.contrib.auth.models import User, Group


def ctx_dict(request):
    ctx = {}
    bitajon = False
    if request.user.groups.filter(name="BITAJON").count():
        bitajon = True
    ctx["bitajon"] = bitajon
    return ctx
