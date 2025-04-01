from django import template

register = template.Library()

@register.filter
def get(obj, attr):
    return getattr(obj, attr, None)