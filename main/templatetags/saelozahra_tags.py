from django import template

import main
from main.models import ProjectFiles
from project.views import percent_icon

register = template.Library()


@register.filter
def darsad(value, arg):
    if arg == 0 or value == 0 or arg is None or value is None:
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
def percent_color_calc(value, arg):
    if value is None:
        value = 0

    if arg is None:
        arg = 0

    if arg == 0 or value == 0:
        our_value = 0
    else:
        our_value = (value * 100) / arg

    print(str(value)+" | "+str(arg)+" | "+str(our_value))

    if our_value == 100:
        color = "darkolivegreen"
    elif our_value == 0:
        color = "indianred"
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
    if value is None or arg is None:
        return 0
    return value - arg


# مرتب سازی کوئری ها
@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.filter()
def marhale_desc(pid, num):
    state_name = "marhale%s" % num
    return main.models.Project.objects.filter(id=pid).get().__dict__.get(state_name)


@register.filter()
def marhale_accomplished(pid, num):
    state_name = "marhale%saccomplished" % num
    print(state_name)
    return main.models.Project.objects.filter(id=pid).get().__dict__.get(state_name)


@register.filter()
def marhale_full(pid, num):
    state_name = "marhale%sfull" % num
    print(state_name)
    return main.models.Project.objects.filter(id=pid).get().__dict__.get(state_name)


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)

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
