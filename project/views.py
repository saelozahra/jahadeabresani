from datetime import timedelta, datetime

from django.core.paginator import Paginator
import jdatetime
from django.http.response import Http404
from django.shortcuts import render

import events.models
import financial.models
import main.models
from django.views.generic import TemplateView
from django.db.models import Q, Sum


# Create your views here.


def percent_icon(numbers, is_percent=True):
    int_number = int(numbers)
    numbers = str(numbers)

    percent_icon_html = ""
    if is_percent:
        percent_icon_html = "<i class='material-icons'>percent</i>"

    if int_number == 100:
        icon = "<i class='material-icons green'>battery_full</i>"
    elif int_number < 10:
        icon = percent_icon_html + "<i class='material-icons'>" + darsad_icon_name(numbers) + "</i>"
    else:
        icon = percent_icon_html + "<i class='material-icons'>" + darsad_icon_name(numbers[:1]) + "</i>" \
                "<i class='material-icons'>" + darsad_icon_name(numbers[1:2]) + "</i>"
    return icon


def darsad_icon_name(numbers):
    if numbers == "0":
        return "exposure_zero"
    else:
        return "filter_"+numbers


class ProjectsPage(TemplateView):

    def get(self, request, **kwargs):
        all_cities = main.models.CityProject.objects.all()
        projects_data = []
        for cd in all_cities:
            projects_data.append({
                'title': cd.city,
                'slug': cd.slug,
                'miangin_pishraft': cd.miangin_pishraft,
                'projects': main.models.Project.objects.filter(Q(RelatedCity__slug__contains=cd.slug)).values(),
            })

        paginator = Paginator(projects_data, 50)  # Show 15 city per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'projects_data': projects_data,
            'page_obj': page_obj,
        }
        return render(request, 'project.html', context)


class SearchPage(TemplateView):

    def post(self, request):
        query = ""
        search_word = self.request.POST['text']
        search_in = self.request.POST['search_in']
        baze_pishraft = self.request.POST['baze_pishraft']
        baze_min = baze_pishraft.split(",")[0]
        baze_max = baze_pishraft.split(",")[1]
        if search_in == "title":
            query = main.models.Project.objects.filter(
                Q(title__contains=search_word, pishrafte_kol__range=(baze_min, baze_max))
            )
        elif search_in == "city":
            query = main.models.Project.objects.filter(
                Q(RelatedCity__slug=search_word, pishrafte_kol__range=(baze_min, baze_max))
                or
                Q(RelatedCity__city__contains=search_word, pishrafte_kol__range=(baze_min, baze_max))
            )
        elif search_in == "admin":
            query = main.models.Project.objects.filter(
                Q(team__first_name__contains=search_word, pishrafte_kol__range=(baze_min, baze_max))
                |
                Q(team__last_name__contains=search_word, pishrafte_kol__range=(baze_min, baze_max))
                |
                Q(team__username__contains=search_word, pishrafte_kol__range=(baze_min, baze_max))
            )
        elif search_in == "project_type":
            query = main.models.Project.objects.filter(
                Q(
                    type__title=search_word,
                    pishrafte_kol__range=(baze_min, baze_max)
                )
            )

        context = {
            'search_in': search_in,
            'search_word': search_word,
            'min': baze_min,
            'max': baze_max,
            'projects_data': query,
            'projects_count': query.exists(),
        }
        print("search_in: "+search_in)
        print("search_word: "+search_word)
        print("baze_pishraft: "+baze_pishraft+" min: "+baze_min+" max: "+baze_max)

        return render(request, 'search.html', context)
        # end method
    # end method

    def get(self, request, **kwargs):
        path_name = request.resolver_match.view_name
        print(path_name)

        if path_name == "promote":
            title = "پروژه‌های ویژه"
            query = main.models.Project.objects.filter(
                Q(promote=True)
            )
        elif path_name == "inactive_today":
            title = "غیرفعال‌های امروز"
            query = main.models.Project.objects.filter(
                Q(last_update__lte=datetime.now() + timedelta(days=1))
            )
        elif path_name == "inactive2month":
            title = "پروژه‌های غیرفعال در دو ماه اخیر"
            query = main.models.Project.objects.filter(
                Q(last_update__lte=datetime.now() + timedelta(days=60))
            )
        elif path_name == "latest_actived":
            title = "امروز فعال بوده"
            query = main.models.Project.objects.filter(
                Q(last_update__month=datetime.month, last_update__day=datetime.day)
            )
        elif path_name == "without_files":
            title = "فاقد مستندات"
            query = main.models.Project.objects.filter(
                Q(Documents__isnull=True)
            )
        elif path_name == "ended":
            title = "تکمیل شده"
            query = main.models.Project.objects.filter(
                Q(pishrafte_kol=100)
            )
        elif path_name == "has_note":
            title = "دارای یادداشت مدیریتی"
            query = main.models.Project.objects.exclude(
                Q(note__exact="") | Q(note__isnull=True)
            )
        elif path_name == "less_than_20":
            title = "پروژه‌های با میانگین پیشرفت کم"
            query = main.models.Project.objects.filter(
                Q(pishrafte_kol__range=(0, 20))
            )
        elif path_name == "more_than_80":
            title = "پروژه‌های با میانگین پیشرفت بالا"
            query = main.models.Project.objects.filter(
                Q(pishrafte_kol__range=(80, 100))
            )
        elif path_name == "without_gharardad":
            title = "پروژه‌های فاقد قرارداد"
            query = main.models.Project.objects.exclude(
                Q(Documents__DocName__exact="gharardad")
            )
        elif path_name == "week_end_date":
            title = "پایان در هفته آینده"
            week_start = datetime.today()
            week_start -= timedelta(days=week_start.weekday())
            week_end = week_start + timedelta(days=7)
            query = main.models.Project.objects.exclude(
                date_end__gte=week_start, date_end__lt=week_end
            )
        elif path_name == "week_end_date":
            title = "پایان در ماه آینده"
            week_start = datetime.today()
            week_start -= timedelta(days=week_start.weekday())
            week_end = week_start + timedelta(days=30)
            query = main.models.Project.objects.exclude(
                date_end__gte=week_start, date_end__lt=week_end
            )
        elif path_name == "object_type":
            objt = kwargs.get("objt")
            title = objt
            query = main.models.Project.objects.filter(
                Q(type__title=objt)
            )
        else:
            query = main.models.Project.objects.all()
            title = "الگویی یافت نشد"

        context = {
            'obj_type': main.models.MapObjectTypes.objects.all().values(),
            'search_in': title,
            'search_word': "",
            'min': 0,
            'max': 100,
            'projects_data': query,
            'projects_count': query.exists(),
        }

        return render(request, 'search.html', context)


class SingleProject(TemplateView):
    def get(self, request, **kwargs):
        pid = int(kwargs.get("pid"))
        this_project = main.models.Project.objects.filter(Q(id=pid))
        if not this_project.exists():
            raise Http404
        this_project.update(view_count=this_project[0].view_count + 1)

        this_project = this_project.get()

        timeline = events.models.Events.objects.filter(Q(RelatedProject_id=pid))
        tl_day = {}

        for tl in timeline:
            tl_day[tl.day.__str__()] = timeline.filter(day=tl.day.__str__())
        # print(tl_day)  # after changes

        context = {
            'toman': '<svg style="width: 32px; height: 32px; fill: var(--color);opacity: 0.4;"> <use xlink:href="#toman"> <symbol id="toman" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 14"><path fill-rule="evenodd" d="M3.057 1.742L3.821 1l.78.75-.776.741-.768-.749zm3.23 2.48c0 .622-.16 1.111-.478 1.467-.201.221-.462.39-.783.505a3.251 3.251 0 01-1.083.163h-.555c-.421 0-.801-.074-1.139-.223a2.045 2.045 0 01-.9-.738A2.238 2.238 0 011 4.148c0-.059.001-.117.004-.176.03-.55.204-1.158.525-1.827l1.095.484c-.257.532-.397 1-.419 1.403-.002.04-.004.08-.004.12 0 .252.055.458.166.618a.887.887 0 00.5.354c.085.028.178.048.278.06.079.01.16.014.243.014h.555c.458 0 .769-.081.933-.244.14-.139.21-.383.21-.731V2.02h1.2v2.202zm5.433 3.184l-.72-.7.709-.706.735.707-.724.7zm-2.856.308c.542 0 .973.19 1.293.569.297.346.445.777.445 1.293v.364h.18v-.004h.41c.221 0 .377-.028.467-.084.093-.055.14-.14.14-.258v-.069c.004-.243.017-1.044 0-1.115L13 8.05v1.574a1.4 1.4 0 01-.287.863c-.306.405-.804.607-1.495.607h-.627c-.061.733-.434 1.257-1.117 1.573-.267.122-.58.21-.937.265a5.845 5.845 0 01-.914.067v-1.159c.612 0 1.072-.082 1.38-.247.25-.132.376-.298.376-.499h-.515c-.436 0-.807-.113-1.113-.339-.367-.273-.55-.667-.55-1.18 0-.488.122-.901.367-1.24.296-.415.728-.622 1.296-.622zm.533 2.226v-.364c0-.217-.048-.389-.143-.516a.464.464 0 00-.39-.187.478.478 0 00-.396.187.705.705 0 00-.136.449.65.65 0 00.003.067c.008.125.066.22.177.283.093.054.21.08.352.08h.533zM9.5 6.707l.72.7.724-.7L10.209 6l-.709.707zm-6.694 4.888h.03c.433-.01.745-.106.937-.29.024.012.065.035.12.068l.074.039.081.042c.135.073.261.133.379.18.345.146.67.22.977.22a1.216 1.216 0 00.87-.34c.3-.285.449-.714.449-1.286a2.19 2.19 0 00-.335-1.145c-.299-.457-.732-.685-1.3-.685-.502 0-.916.192-1.242.575-.113.132-.21.284-.294.456-.032.062-.06.125-.084.191a.504.504 0 00-.03.078 1.67 1.67 0 00-.022.06c-.103.309-.171.485-.205.53-.072.09-.214.14-.427.147-.123-.005-.209-.03-.256-.076-.057-.054-.085-.153-.085-.297V7l-1.201-.5v3.562c0 .261.048.496.143.703.071.158.168.296.29.413.123.118.266.211.43.28.198.084.42.13.665.136v.001h.036zm2.752-1.014a.778.778 0 00.044-.353.868.868 0 00-.165-.47c-.1-.134-.217-.201-.35-.201-.18 0-.33.103-.447.31-.042.071-.08.158-.114.262a2.434 2.434 0 00-.04.12l-.015.053-.015.046c.142.118.323.216.544.293.18.062.325.092.433.092.044 0 .086-.05.125-.152z" clip-rule="evenodd"></path></symbol></use></svg>',
            'id': pid,
            'project': this_project.maraheleejra_set,
            'marahel_ejra': main.models.MaraheleEjra.objects.filter(Q(Project_id=pid)),
            'tl_day': tl_day,
            'doc_type': main.models.ProjectFiles.DocChoices,
            'lat': this_project.location.split(",")[0],
            'lng': this_project.location.split(",")[1],
            'finance': financial.models.PPP.objects.filter(ForProject_id=pid),
            'finance_sum': financial.models.PPP.objects.filter(ForProject_id=pid).aggregate(Sum('CommodityPrice')),
            'icon': percent_icon(this_project.pishrafte_kol),
        }
        return render(request, 'project-single.html', context)
