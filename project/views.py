from django.http.response import Http404
from django.shortcuts import render
import main.models
from django.views.generic import TemplateView
from django.db.models import Q
# Create your views here.


def darsad_icon(self, numbers):
    numbers = str(numbers)
    if numbers == 100:
        icon = "<i class='material-icons'>battery_full</i>"
    elif numbers.__len__() > 1:
        icon = "<i class='material-icons'>percent</i>" \
               "<i class='material-icons'>" + darsad_icon(self, numbers) + "</i>"
    else:
        icon = "<i class='material-icons'>percent</i>" \
               "<i class='material-icons'>" + darsad_icon_name(self, numbers[:1]) + "</i>" \
                "<i class='material-icons'>" + darsad_icon_name(self, numbers[1:2]) + "</i>"
    return icon


def darsad_icon_name(self, numbers):
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
        context = {'projects_data': projects_data}
        return render(request, 'project.html', context)


class SearchPage(TemplateView):

    def post(self, request):
        search_word = self.request.POST['text']
        print("search_word: "+search_word)
        context = {'projects_data': main.models.Project.objects.filter(Q(title__contains=search_word))}
        return render(request, 'search.html', context)


class SingleProject(TemplateView):
    def get(self, request, **kwargs):
        pid = int(kwargs.get("pid"))
        this_project = main.models.Project.objects.filter(Q(id=pid))
        if not this_project.exists():
            raise Http404
        this_project.update(view_count=this_project[0].view_count + 1)

        this_project = this_project.get()

        context = {
            'project': this_project,
            'lat': this_project.location.split(",")[0],
            'lng': this_project.location.split(",")[1],
            'icon': darsad_icon(self, this_project.pishrafte_kol),
        }
        return render(request, 'project-single.html', context)
