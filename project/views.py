from django.shortcuts import render
import main.models
from main.models import *
# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.views.generic import TemplateView
from django.db.models import Q

def darsad_icon(self,adad):
    if adad == "0":
        return "exposure_zero"
    else:
        return "filter_"+adad
    
    
class project(TemplateView):
    def post(self, request):
        search_word = self.request.POST['text']
        print(search_word)
        search_projects_data = []
        search_in_projects_query = main.models.project.objects.filter(Q(title__contains=search_word))
        for spd in search_in_projects_query:
            search_projects_data.append({
                'title': spd.title,
                'city': spd.city,
                'photo': spd.photo.url,
                'slug': spd.slug,
                'miangin_pishraft': spd.miangin_pishraft,
                'date_start': spd.date_start,
                'date_end': spd.date_end,
            })
        context = {'projects_data': search_projects_data}
        return render(request, 'project.html', context)
    def get(self, request):
        projects_data = []
        all_projects = main.models.project.objects.all()
        for pd in all_projects:
            projects_data.append({
                'title': pd.title,
                'city': pd.city,
                'photo': pd.photo.url,
                'slug': pd.slug,
                'miangin_pishraft': pd.miangin_pishraft,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
            })
        context = {'projects_data': projects_data}
        return render(request, 'project.html', context)

class single_project(TemplateView):
    def get(self,request,slug):
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

        main.models.project.objects.filter(slug=slug).update(miangin_pishraft=miangin_pishrafte_kol)

        for pd in all_projects:
            all_projects.update(view_count=(pd.view_count)+1)
            final_data = {
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
                'note': pd.note,
                'subprojects': subprojects_data,
                'miangin_pishraft': miangin_pishrafte_kol,
                'user_login': self.request.user.is_authenticated,
                'user_id': self.request.user.id,
                'view_count': pd.view_count,
            }
        print(final_data)
        return render(request, 'project-single.html', {'projects_data': final_data})
class single_sub_project(TemplateView):
    def get(self, request, slug , id):
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
                'naghshe': pd.naghshe.url,
                'mostanadat': pd.mostanadat.url,
                'mojavez': pd.mojavez.url,
                'file_ha': pd.file_ha.url,
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
