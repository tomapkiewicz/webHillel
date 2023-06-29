from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Page,RecurrentPage
from .cuestionario import Cuestionario, CuestionarioRespuesta
from .subscription import Subscription
from .responsable import Responsable
from .historial import Historial
from .colaborador import Colaborador

from django.contrib.admin import  SimpleListFilter
from .forms import RecurrentPageForm, PageForm

class ModalidadFilter(SimpleListFilter):
    title = "Modalidad"  # a label for our filter
    parameter_name = "modalidad"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            (0, "Presencial"),
            (1, "Online"),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() is None: return queryset.all() 
        return queryset.distinct().filter(modalidad=self.value())


# Register your models here.
class CuestionarioAdmin(admin.ModelAdmin):
    list_display = ('page', 'updated',)
    search_fields = ('page__title',)


class CuestionarioRespuestaAdmin(admin.ModelAdmin):
    list_display = ('page', 'user', 'updated')
    search_fields = ('page__title', 'user__username')

# Register your models here.


class HistorialAdmin(admin.ModelAdmin):
    list_display = ('page', 'fecha', 'Qasistentes', 'Qanotados')
    search_fields = ('page__title', 'fecha')
    readonly_fields = ('anotados',)

class PageAdmin(admin.ModelAdmin):
    list_display = ('actividadSTR', 'fecha', 'provincia', 'cupo', 'Qanotados', 'secreta', 'activa', 'horaDesde')
    search_fields = ('title', 'fecha', 'activa', 'secreta', 'provincia__title',)
    list_filter = (ModalidadFilter, 'fecha', 'activa', 'secreta', 'horaDesde', 'cupo', 'provincia')
    form = PageForm  # Assuming you have a custom form for Page

    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            # If it's a new object, create corresponding RecurrentPages
            create_pages(form.instance)


class RecurrentPageAdmin(admin.ModelAdmin):
    list_display = ('actividadSTR', 'fechaDesde', 'fechaHasta', 'provincia', 'cupo', 'secreta', 'activa', 'horaDesde')
    search_fields = ('title', 'fechaDesde', 'fechaHasta', 'activa', 'secreta', 'provincia__title',)
    list_filter = ('fechaDesde', 'fechaHasta', 'activa', 'secreta', 'horaDesde', 'cupo', 'provincia')
    form = RecurrentPageForm 

    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated')
    search_fields = ('user__username',)


class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


admin.site.register(CuestionarioRespuesta, CuestionarioRespuestaAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(RecurrentPage, RecurrentPageAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Colaborador, ColaboradorAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]
