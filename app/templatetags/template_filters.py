from django import template

register = template.Library()

@register.filter(name='replace_dash')
def replace_dash(value, arg):
    return value.replace(arg, ' ')
