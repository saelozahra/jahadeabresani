from django import template
from main.models import ProjectFiles
from project.views import percent_icon

register = template.Library()


@register.filter
def darsad(value, arg):
    if arg == 0 or value == 0:
        return 0
    our_value = (value * 100) / arg

    print(str(value)+" | "+str(arg)+" | "+str(our_value))

    return our_value


def multiply(value, arg):
    return value * arg


@register.filter
def pd_name(value):
    tuple_choice = ProjectFiles.DocChoices
    val = dict(tuple_choice).get(value)
    return val


@register.filter
def percent_color(value):
    if value == 100:
        color = "darkolivegreen"
    elif value == 0:
        color = "darkred"
    else:
        color = "darkgoldenrod"
    return color


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


# مرتب سازی کوئری ها
@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

# @register.filter()
# def var_num(arg, num):
#     if arg == "simple":
#         var = "marhale{}".format(num)
#     elif arg == "full":
#         var = "marhale{}full".format(num)
#     elif arg == "com":
#         var = "marhale{}accomplished".format(num)
#     else:
#         var = "marhale{}".format(num)
#     print(var)
#     return var
