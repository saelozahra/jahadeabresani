from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

import main.models


class index(TemplateView):
    def get(self,request):
        from django.db.models import Q
        projects_data = []
        all_projects = main.models.project.objects.all()
        for pd in all_projects:
            subs = main.models.subproject.objects.filter(Q(project_id__slug__contains=pd.slug))
            miangin_pishrafte_kol = 0
            for spd in subs:
                miangin_pishrafte_kol += spd.pishrafte_kol
            try:
                miangin_pishrafte_kol = miangin_pishrafte_kol / subs.count()
            except:
                miangin_pishrafte_kol = 0
                print("miangin error dade")
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
                'miangin_pishraft': miangin_pishrafte_kol,
            })
        print(projects_data)
        context = {'projects_data': projects_data}
        return render(request, 'index.html', context)
