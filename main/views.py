from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class index(TemplateView):
    def get(self,request):

        return render(request, 'index.html')