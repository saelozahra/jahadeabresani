from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

import city.models
import main.models
from project.views import darsad_icon
# Create your views here.


class SingleCity(TemplateView):
    def get(self, request, slug, **kwargs):
        final_data = []
        all_cities = city.models.CityProject.objects.filter(Q(slug__contains=slug))
        projects_data = []
        this_city_projects = main.models.Project.objects.filter(Q(RelatedCity__slug__contains=slug))

        for pd in this_city_projects:
            icon = darsad_icon(self, pd.pishrafte_kol)
            projects_data.append({
                'id': pd.id,
                'title': pd.title,
                'type':  pd.type,
                'city':  pd.RelatedCity.city,
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
                'projects_count': projects_data.__len__(),
                'miangin_pishraft': cd.miangin_pishraft,
                'user_login': self.request.user.is_authenticated,
                'user_id': self.request.user.id,
                'view_count': cd.view_count,
            }

        print(final_data)
        return render(request, 'city.html', final_data)

