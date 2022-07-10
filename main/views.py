from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

import main.models


class index(TemplateView):
    def get(self,request):
        from django.db.models import Q
        projects_data = []
        all_projects = main.models.project.objects.all()
        miangin_pishrafte_all_projects = 0
        for pd in all_projects:
            subs = main.models.subproject.objects.filter(Q(project_id__slug__contains=pd.slug))
            miangin_pishrafte_project = 0
            for spd in subs:
                miangin_pishrafte_project += spd.pishrafte_kol
            try:
                miangin_pishrafte_project = miangin_pishrafte_project / subs.count()
            except:
                miangin_pishrafte_project = 0
                print("miangin error dade")
            miangin_pishrafte_all_projects += miangin_pishrafte_project
            projects_data.append({
                'title': pd.title,
                'city': pd.city,
                'location': pd.location,
                'lat': pd.location.split(",")[0],
                'lng': pd.location.split(",")[1],
                'photo': pd.photo.url,
                'slug': pd.slug,
                'date_start': pd.date_start,
                'date_end': pd.date_end,
                'sub_project': subs,
                'miangin_pishraft': miangin_pishrafte_project,
            })

        context = {
            'projects_data': projects_data,
            "pishraft": miangin_pishrafte_all_projects/all_projects.count(),
            "projects_number": all_projects.count()
        }
        return render(request, 'index.html', context)
