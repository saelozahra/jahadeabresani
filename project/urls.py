from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.ProjectsPage.as_view(), name="Project"),
    path('project/<pid>', views.SingleProject.as_view(), name="single_sub_project"),
    path('search/', views.SearchPage.as_view(), name="search"),
]
