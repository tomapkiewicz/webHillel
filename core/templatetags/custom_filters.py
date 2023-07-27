from django import template
import calendar

register = template.Library()


@register.filter
def weekday_name(date):
    spanish_weekdays = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábados",
        "domingos",
    ]
    return spanish_weekdays[date.weekday()]
