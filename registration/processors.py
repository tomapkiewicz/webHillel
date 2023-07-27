from .models import TemporadaOnward


def ctx_dict(request):
    ctx = {}

    temporadaOnward = TemporadaOnward.objects.all().first()
    ctx["temporadaOnward"] = temporadaOnward.temporada

    return ctx
