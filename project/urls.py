from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.Project.as_view(), name="Project"),
    path('project/<slug>', views.SingleProject.as_view(), name="SinglProject"),
    path('project/<slug>/<id>', views.SingleSubProject.as_view(), name="single_sub_project"),
    path('search/', views.Project.as_view(), name="search"),
]
