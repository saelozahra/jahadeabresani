from django.shortcuts import render
import main.models
# Create your views here.
from django.views.generic import TemplateView
from django.db.models import Q


def darsad_icon(self, adad):
    adad = str(adad)
    if adad == 100:
        icon = "<i class='material-icons'>battery_full</i>"
    elif adad.__len__()>1:
        icon = "<i class='material-icons'>percent</i>" \
               "<i class='material-icons'>" + darsad_icon(self, adad) + "</i>"
    else:
        icon = "<i class='material-icons'>percent</i>" \
               "<i class='material-icons'>" + darsad_icon_name(self, adad[:1]) + "</i>" \
                "<i class='material-icons'>" + darsad_icon_name(self, adad[1:2]) + "</i>"
    return icon


def darsad_icon_name(self,adad):
    if adad == "0":
        return "exposure_zero"
    else:
        return "filter_"+adad


def calc_proj_values(self, search):
    if search == "":
        all_cities = main.models.CityProject.objects.all()
    else:
        print("search_word: "+search)
        all_cities = main.models.CityProject.objects.filter(Q(title__contains=search))

    projects_data = []
    for pd in all_cities:
        projects_data.append({
            'title': pd.title,
            'city': pd.city,
            'photo': pd.photo.url,
            'slug': pd.slug,
            'miangin_pishraft': pd.miangin_pishraft,
            'sub_projects': main.models.Project.objects.filter(Q(project_id__slug__contains=pd.slug)).values(),
        })
    context = {'projects_data': projects_data}
    return context


class Project(TemplateView):

    def post(self, request):
        search_word = self.request.POST['text']
        return render(request, 'project.html', calc_proj_values(self, search_word))

    def get(self, request):
        return render(request, 'project.html', calc_proj_values(self, ""))


class SingleProject(TemplateView):
    def get(self, request, slug, **kwargs):
        final_data=[]
        all_cities = main.models.CityProject.objects.filter(Q(slug__contains=slug))
        subprojects_data = []
        this_sub_projects = main.models.Project.objects.filter(Q(project_id__slug__contains=slug))
        for pd in this_sub_projects:
            icon = darsad_icon(self, pd.pishrafte_kol)
            subprojects_data.append({
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

        for pd in all_cities:
            all_cities.update(view_count=(pd.view_count)+1)
            final_data = {
                'title': pd.title,
                'city': pd.city,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'slug': pd.slug,
                'note': pd.note,
                'subprojects': subprojects_data,
                'miangin_pishraft': pd.miangin_pishraft,
                'user_login': self.request.user.is_authenticated,
                'user_id': self.request.user.id,
                'view_count': pd.view_count,
            }
        print(final_data)
        return render(request, 'project-single.html', {'projects_data': final_data})


class SingleSubProject(TemplateView):
    def get(self, request, slug, id):
        final_data=[]
        all_cities = main.models.Project.objects.filter(Q(slug__contains=slug))
        subprojects_data = []
        this_sub_projects = main.models.Project.objects.filter(Q(project_id__slug__contains=slug))
        this_single_sub_projects = main.models.Project.objects.filter(id=id)
        for pd in this_sub_projects:
            icon = darsad_icon(self, pd.pishrafte_kol)

            if pd.naghshe :
                naghshe = pd.naghshe.url
            else:
                naghshe = ""

            if pd.mostanadat :
                mostanadat = pd.mostanadat.url
            else:
                mostanadat = ""

            if pd.mojavez :
                mojavez = pd.mojavez.url
            else:
                mojavez = ""

            if pd.file_ha :
                file_ha = pd.file_ha.url
            else:
                file_ha = ""

            subprojects_data.append({
                'id': pd.id,
                'title': pd.title,
                'type': pd.type,
                'photo': pd.photo.url,
                'naghshe': naghshe,
                'mostanadat': mostanadat,
                'mojavez': mojavez,
                'file_ha': file_ha,
                'pishrafte_kol': pd.pishrafte_kol,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'team': pd.team,
                'icon': icon,
                'view_count': pd.view_count,
            })
        for pd in all_cities:

            all_cities.update(view_count=pd.view_count + 1)
            final_data = {
                'sp_id': id,
                'title': pd.title,
                'city': pd.city,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'slug': pd.slug,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'subprojects': subprojects_data,
                'this_single_sub_projects': this_single_sub_projects,
                'miangin_pishraft': pd.miangin_pishraft,
                'view_count': pd.view_count,
            }
        print(final_data)
        return render(request, 'subproject-single.html', {'projects_data': final_data})
