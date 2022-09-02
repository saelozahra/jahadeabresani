from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('city/<slug>', views.SingleCity.as_view(), name="SingleCity"),
    path('project/', views.ProjectsPage.as_view(), name="Project"),
    path('project/<id>', views.SingleProject.as_view(), name="single_sub_project"),
    path('search/', views.ProjectsPage.as_view(), name="search"),
]
