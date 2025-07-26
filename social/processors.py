from .models import Link, Whatsapp


def ctx_dict(request):
    ctx = {}
    links = Link.objects.all()
    for link in links:
        ctx[link.key] = link.url
    whatsapp = Whatsapp.objects.all().first()
    ctx["whatsappHillel"] = whatsapp

    return ctx

from .models import Link, Whatsapp

def ctx_dict(request):
    ctx = {}
    links = Link.objects.all()
    for link in links:
        ctx[link.key] = link.url

    whatsapp_numero = ""  # Default value if no user is authenticated or no specific province is set

    if request.user.is_authenticated:
        provincia = request.user.profile.provincia 
        personalizado = Whatsapp.objects.filter(name__iexact=provincia).first()
        if personalizado:
            whatsapp_numero = personalizado.numero
        else:
            default = Whatsapp.objects.filter(name__iexact="Buenos Aires (CABA GBA)").first()
            if default:
                whatsapp_numero = default.numero
    else:
        default = Whatsapp.objects.filter(name__iexact="Buenos Aires (CABA GBA)").first()
        if default:
            whatsapp_numero = default.numero

    ctx["whatsappHillel"] = whatsapp_numero
    return ctx