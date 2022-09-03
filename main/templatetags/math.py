from django import template
from main.models import ProjectFiles

register = template.Library()


@register.filter
def darsad(value, arg):
    if arg == 0 or value == 0:
        return 0
    return (value * 100) / arg


def multiply(value, arg):
    return value * arg


@register.filter
def pd_name(value):
    tuple_choice = ProjectFiles.DocChoices
    val = dict(tuple_choice).get(value)
    return val


@register.filter
def menha(value, arg):
    return value - arg
