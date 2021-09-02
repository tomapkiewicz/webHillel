from django.contrib import admin
from .models import Link, Whatsapp, MailContacto


# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    def get_readonly_fields(self, request, obj=None):
        # if request.user.groups.filter(name='admin').exists():
        if request.user.is_superuser:
            return ('created', 'updated')
        else:
            return ('key', 'name')


class WhatsappAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    def get_readonly_fields(self, request, obj=None):
        # if request.user.groups.filter(name='admin').exists():
        if request.user.is_superuser:
            return ('created', 'updated')
        else:
            return ('name')


class MailContactoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    def get_readonly_fields(self, request, obj=None):
        # if request.user.groups.filter(name='admin').exists():
        if request.user.is_superuser:
            return ('created', 'updated')
        else:
            return ('mail')


admin.site.register(Link, LinkAdmin)
admin.site.register(Whatsapp, WhatsappAdmin)
admin.site.register(MailContacto, MailContactoAdmin)
