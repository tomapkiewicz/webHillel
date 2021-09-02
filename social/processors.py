from .models import Link, MailContacto, Whatsapp


def ctx_dict(request):
    ctx = {}
    links = Link.objects.all()
    for link in links:
        ctx[link.key] = link.url
    whatsapp = Whatsapp.objects.all().first()
    ctx['whatsappHillel'] = whatsapp

    return ctx
