from django.shortcuts import render
import main.models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ApiSaveProjectNote(APIView):
    def post(self , request , format=None):
        try:
            PSlug = self.request.POST['project']
            note  = self.request.POST['text']
            print(PSlug)
            print(note)
            main.models.project.objects.filter(slug=PSlug).update(note=note)
            return Response({"response":"ok"},status=status.HTTP_200_OK)
        except:
            return Response({"response":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self , request , format=None):
        try:
            projects_data = []
            all_projects = main.models.project.objects.all()
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
            return Response({"response":projects_data},status=status.HTTP_200_OK)
        except:
            return Response({"response":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)