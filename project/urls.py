from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.ProjectsPage.as_view(), name="Project"),
    path('project/<pid>', views.SingleProject.as_view(), name="single_sub_project"),
    path('search/', views.SearchPage.as_view(), name="search"),
    path('search/inactive2month', views.SearchPage.as_view(), name="inactive2month"),
    path('search/less_than_20', views.SearchPage.as_view(), name="less_than_20"),
    path('search/more_than_80', views.SearchPage.as_view(), name="more_than_80"),
]
