from django.contrib import admin
from .models import Profile, FechaOnward, FechaTaglit, PropuestaInteres, TematicaInteres, TemporadaOnward
from pages.models import Day, Category

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'apellido', 'edad', 'whatsapp', 'provincia',)
    search_fields = ('apellido','nombre','user__username','provincia__title')


class FechaTaglitAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class PropuestaInteresAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class TematicaInteresAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class FechaOnwardAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class TemporadaOnwardAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class DayAdmin(admin.ModelAdmin):
    list_display = ('day',)


class CategoriesAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


admin.site.register(PropuestaInteres, PropuestaInteresAdmin)
admin.site.register(TematicaInteres, TematicaInteresAdmin)
admin.site.register(FechaTaglit, FechaTaglitAdmin)
admin.site.register(FechaOnward, FechaOnwardAdmin)
admin.site.register(TemporadaOnward, TemporadaOnwardAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Category, CategoriesAdmin)
