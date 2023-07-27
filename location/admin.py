from django.contrib import admin
from .models import Provincia


# Register your models here.
class ProvinciaAdmin(admin.ModelAdmin):
    readonly_fields = ("updated", "created")


admin.site.register(Provincia, ProvinciaAdmin)
