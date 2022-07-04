from django.shortcuts import render
import main.models
from main.models import *
# Create your views here.
from django.views.generic import TemplateView

def darsad_icon(self,adad):
    if adad == "0":
        return "exposure_zero"
    else:
        return "filter_"+adad
class project(TemplateView):
    def get(self, request):
        projects_data = []
        all_projects = main.models.project.objects.all()
        for pd in all_projects:
            projects_data.append({
                'title': pd.title,
                'city': pd.city,
                'photo': pd.photo.url,
                'slug': pd.slug,
                'date_end': pd.date_end,
            })
        # context = {'projects_data': projects_data}
        return render(request, 'project.html', {'projects_data': projects_data})
class single_project(TemplateView):
    def get(self,request,slug):
        from django.db.models import Q
        all_projects = main.models.project.objects.filter(Q(slug__contains=slug))
        subprojects_data = []
        this_sub_projects = main.models.subproject.objects.filter(Q(project_id__slug__contains=slug))
        miangin_pishrafte_kol = 0
        for pd in this_sub_projects:
            miangin_pishrafte_kol += pd.pishrafte_kol
            if pd.pishrafte_kol == 100:
                icon = "<i class='material-icons'>battery_full</i>"
            elif pd.pishrafte_kol < 10:
                icon = "<i class='material-icons'>percent</i><i class='material-icons'>"+darsad_icon(self,str(pd.pishrafte_kol))+"</i>"
            else:
                icon = "<i class='material-icons'>percent</i><i class='material-icons'>"+darsad_icon(self,str(pd.pishrafte_kol)[:1])+"</i><i class='material-icons'>"+darsad_icon(self,str(pd.pishrafte_kol)[1:2])+"</i>"
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

        try:
            miangin_pishrafte_kol = miangin_pishrafte_kol / this_sub_projects.count()
            print(miangin_pishrafte_kol)
            print(miangin_pishrafte_kol)
            print(this_sub_projects.count())
        except:
            miangin_pishrafte_kol = 0
            print("miangin error dade")

        for pd in all_projects:
            all_projects.update(view_count=(pd.view_count)+1)
            final_data = {
                'title': pd.title,
                'city': pd.city,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'naghshe': pd.naghshe.url,
                'mojavez': pd.mojavez.url,
                'mostanadat': pd.mostanadat.url,
                'file_ha': pd.file_ha.url,
                'slug': pd.slug,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'subprojects': subprojects_data,
                'miangin_pishraft': miangin_pishrafte_kol,
                'view_count': pd.view_count,
            }
        print(final_data)
        return render(request, 'project-single.html', {'projects_data': final_data})


class single_sub_project(TemplateView):
    def get(self, request, slug , id):
        from django.db.models import Q
        all_projects = main.models.project.objects.filter(Q(slug__contains=slug))
        subprojects_data = []
        this_sub_projects = main.models.subproject.objects.filter(Q(project_id__slug__contains=slug))
        this_single_sub_projects = main.models.subproject.objects.filter(id=id)
        miangin_pishrafte_kol = 0
        for pd in this_sub_projects:
            miangin_pishrafte_kol += pd.pishrafte_kol
            if pd.pishrafte_kol == 100:
                icon = "<i class='material-icons'>battery_full</i>"
            elif pd.pishrafte_kol < 10:
                icon = "<i class='material-icons'>percent</i><i class='material-icons'>" + darsad_icon(self,
                                                                                                       str(pd.pishrafte_kol)) + "</i>"
            else:
                icon = "<i class='material-icons'>percent</i><i class='material-icons'>" + darsad_icon(self,
                                                                                                       str(pd.pishrafte_kol)[
                                                                                                       :1]) + "</i><i class='material-icons'>" + darsad_icon(
                    self, str(pd.pishrafte_kol)[1:2]) + "</i>"
            subprojects_data.append({
                'id': pd.id,
                'title': pd.title,
                'type': pd.type,
                'photo': pd.photo.url,
                'pishrafte_kol': pd.pishrafte_kol,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'team': pd.team,
                'icon': icon,
                'view_count': pd.view_count,
            })
        try:
            miangin_pishrafte_kol = miangin_pishrafte_kol / this_sub_projects.count()
            print(miangin_pishrafte_kol)
            print(miangin_pishrafte_kol)
            print(this_sub_projects.count())
        except:
            miangin_pishrafte_kol = 0
            print("miangin error dade")
        for pd in all_projects:
            all_projects.update(view_count=(pd.view_count) + 1)
            final_data = {
                'sp_id': id,
                'title': pd.title,
                'city': pd.city,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'mojavez': pd.mojavez.url,
                'mostanadat': pd.mostanadat.url,
                'file_ha': pd.file_ha.url,
                'slug': pd.slug,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'subprojects': subprojects_data,
                'this_single_sub_projects': this_single_sub_projects,
                'miangin_pishraft': miangin_pishrafte_kol,
                'view_count': pd.view_count,
            }
        print(final_data)
        return render(request, 'subproject-single.html', {'projects_data': final_data})
