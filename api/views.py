from django.shortcuts import render

import city.models
import main.models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class ApiSaveCityNote(APIView):

    def post(self, request, format=None):
        try:
            pid = self.request.POST['city']
            note = self.request.POST['text']
            print(pid)
            print(note)
            city.models.CityProject.objects.filter(slug=pid).update(note=note)
            return Response({"response": "ok"}, status=status.HTTP_200_OK)
        except NameError:
            print(NameError)
            return Response({"response": NameError}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            projects_data = []
            all_projects = city.models.CityProject.objects.all()
            for pd in all_projects:
                projects_data.append({
                    'id': pd.id,
                    'city': pd.city,
                    'slug': pd.slug,
                    'miangin_pishraft': pd.miangin_pishraft,
                    'view_count': pd.view_count,
                    'note': pd.note,
                })
            return Response({"response": projects_data}, status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiSaveProjectNote(APIView):

    def post(self, request, format=None):
        try:
            pid = self.request.POST['project']
            note = self.request.POST['text']
            print(pid)
            print(note)
            main.models.Project.objects.filter(id=pid).update(note=note)
            return Response({"response": "ok"},status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            projects_data = []
            all_projects = main.models.Project.objects.all()
            for pd in all_projects:
                projects_data.append({
                    'id': pd.id,
                    'title': pd.title,
                    'slug': pd.slug,
                    'photo': pd.photo.url,
                    'city': pd.city,
                    'location': pd.location,
                    'miangin_pishraft': pd.miangin_pishraft,
                    'date_start': str(pd.date_start.year) + "/" + str(pd.date_start.month) + "/" + str(pd.date_start.day),
                    'date_end': str(pd.date_end.year) + "/" + str(pd.date_end.month) + "/" + str(pd.date_end.day),
                    'mojavez': pd.mojavez.url,
                    'mostanadat': pd.mostanadat.url,
                    'file_ha': pd.file_ha.url,
                    'note': pd.note,
                    'view_count': pd.view_count,
                })
            return Response({"response": projects_data}, status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiProjectType(APIView):

    def get(self, request, pt_id, format=None):
        try:
            print("pt_id: "+pt_id)
            all_map_obj_types_data = []
            all_marahel_ejra_data = []
            all_map_obj_types = main.models.MapObjectTypes.objects.filter(id=pt_id)
            for pd in all_map_obj_types:
                mejr_all = pd.marhalel_ejra_s.all()
                for me in mejr_all:
                    all_marahel_ejra_data.append(me.marhale)
                all_map_obj_types_data = {
                    'id': pd.id,
                    'title': pd.title,
                    'icon': pd.icon.url,
                    'marahel': all_marahel_ejra_data,
                    'marahel_count': pd.marhalel_ejra_s.count(),
                }
            if all_map_obj_types.count() == 0:
                return Response({"response": "noting found any value"}, status=status.HTTP_200_OK)
            else:
                return Response(all_map_obj_types_data, status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
