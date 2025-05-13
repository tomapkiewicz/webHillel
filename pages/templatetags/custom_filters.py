from django import template

register = template.Library()

@register.filter
def get(obj, attr):
    return getattr(obj, attr, None)

@register.filter
def contains(queryset, item):
    return item in queryset
