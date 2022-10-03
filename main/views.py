from django.shortcuts import render
from django.views.generic import TemplateView
import main.models


# Create your views here.


class Index(TemplateView):
    def get(self, request, **kwargs):
        projects_data = []
        all_projects = main.models.Project.objects.all()
        miangin_pishrafte_all_projects = 0
        for pd in all_projects:
            miangin_pishrafte_all_projects += pd.pishrafte_kol
            projects_data.append({
                'id': pd.id,
                'title': pd.title,
                'city': pd.RelatedCity,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'icon': pd.type.icon.url,
                'last_update': pd.last_update,
                'promote': pd.promote,
                'miangin_pishraft': pd.pishrafte_kol,
            })

        try:
            miangin_pishrafte_all_projects = miangin_pishrafte_all_projects / all_projects.count()
        except:
            miangin_pishrafte_all_projects = 0

        context = {
            'projects_data': projects_data,
            'obj_type': main.models.MapObjectTypes.objects.all(),
            "pishraft": miangin_pishrafte_all_projects,
            "projects_number": all_projects.count(),
            "projects": all_projects
        }
        return render(request, 'index.html', context)
