from django import template

register = template.Library()

@register.filter(name='floor_divide')
def floor_divide(value, divisor):
    return value // divisor