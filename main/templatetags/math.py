from django import template

register = template.Library()


@register.filter
def darsad(value, arg):
    if arg == 0 or value == 0:
        return 0
    return (value * 100) / arg


def multiply(value, arg):
    return value * arg


@register.filter
def menha(value, arg):
    return value - arg
