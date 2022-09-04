from django import template
from main.models import ProjectFiles
from project.views import percent_icon

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
def filter_number_icon(value, arg=0):
    is_percent = False
    if arg == 1:
        is_percent = True
    darsad_icon_html = percent_icon(value, is_percent)
    darsad_icon_html = "<div class='ltr'>" + darsad_icon_html + "</div>"
    return darsad_icon_html


@register.filter
def menha(value, arg):
    return value - arg
