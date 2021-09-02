from django.contrib import admin
from .models import Profile, FechaOnward, FechaTaglit
from pages.models import Day, Category

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'apellido', 'edad', 'whatsapp', 'provincia',)
    readonly_fields = ('updated', 'created')
    search_fields = ('page__title', 'fecha')


class FechaTaglitAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class FechaOnwardAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


class DayAdmin(admin.ModelAdmin):
    list_display = ('day',)


class CategoriesAdmin(admin.ModelAdmin):
    readonly_fields = ('updated', 'created')


admin.site.register(FechaTaglit, FechaTaglitAdmin)
admin.site.register(FechaOnward, FechaOnwardAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Category, CategoriesAdmin)
