from django.contrib import admin
from .models import Page, Subscription, Historial,Responsable, Colaborador, Cuestionario, CuestionarioRespuesta
from django.contrib.admin.models import LogEntry


# Register your models here.
class CuestionarioAdmin(admin.ModelAdmin):
    list_display = ('page', 'updated' ,)
    search_fields = ('page__title',)
    
class CuestionarioRespuestaAdmin(admin.ModelAdmin):
    list_display = ('page', 'user','updated' )
    search_fields = ('page__title', 'user__username')

# Register your models here.
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('page', 'fecha','Qasistentes','Qanotados' )
    search_fields = ('page__title', 'fecha')
    readonly_fields = ('anotados',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('actividadSTR', 'dia','provincia', 'cupo', 'Qanotados','secreta', 'activa','horaDesde')
    search_fields = ('title', 'dia__day', 'activa','secreta','provincia__title',)

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
