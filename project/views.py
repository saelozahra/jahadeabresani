from django.shortcuts import render
import main.models
# Create your views here.
from django.views.generic import TemplateView
from django.db.models import Q


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


def calc_proj_values(self, search):
    if search == "":
        all_cities = main.models.CityProject.objects.all()
    else:
        print("search_word: "+search)
        all_cities = main.models.CityProject.objects.filter(Q(title__contains=search))

    projects_data = []
    for cd in all_cities:
        projects_data.append({
            'title': cd.city,
            'slug': cd.slug,
            'miangin_pishraft': cd.miangin_pishraft,
            'projects': main.models.Project.objects.filter(Q(RelatedCity__slug__contains=cd.slug)).values(),
        })
    context = {'projects_data': projects_data}
    return context


class ProjectsPage(TemplateView):

    def post(self, request):
        search_word = self.request.POST['text']
        return render(request, 'project.html', calc_proj_values(self, search_word))

    def get(self, request, **kwargs):
        return render(request, 'project.html', calc_proj_values(self, ""))


class SingleCity(TemplateView):
    def get(self, request, slug, **kwargs):
        final_data = []
        all_cities = main.models.CityProject.objects.filter(Q(slug__contains=slug))
        projects_data = []
        this_city_projects = main.models.Project.objects.filter(Q(RelatedCity__slug__contains=slug))

        for pd in this_city_projects:
            icon = darsad_icon(self, pd.pishrafte_kol)
            projects_data.append({
                'id': pd.id,
                'title': pd.title,
                'type':  pd.type,
                'photo':  pd.photo.url,
                'pishrafte_kol':  pd.pishrafte_kol,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'team': pd.team,
                'icon': icon,
                'view_count': pd.view_count,
            })

        for cd in all_cities:
            all_cities.update(view_count=cd.view_count + 1)
            final_data = {
                'city': cd.city,
                'slug': cd.slug,
                'projects': projects_data,
                'miangin_pishraft': cd.miangin_pishraft,
                'user_login': self.request.user.is_authenticated,
                'user_id': self.request.user.id,
                'view_count': cd.view_count,
            }

        print(final_data)
        return render(request, 'city-single.html', {'projects_data': final_data})


class SingleProject(TemplateView):
    def get(self, request, slug, pid):
        final_data = []
        this_project = main.models.Project.objects.filter(Q(id=pid))
        for pd in this_project:
            icon = darsad_icon(self, pd.pishrafte_kol)

            final_data.append({
                'id': pd.id,
                'title': pd.title,
                'type': pd.type,
                'photo': pd.photo.url,
                'documents': pd.Documents,
                'pishrafte_kol': pd.pishrafte_kol,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'team': pd.team,
                'icon': icon,
                'view_count': pd.view_count,
            })
        return render(request, 'project-single.html', {'projects_data': final_data})
