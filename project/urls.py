from django.urls import path
from . import views
urlpatterns = [
    path('project/', views.ProjectsPage.as_view(), name="Project"),
    path('project/<pid>', views.SingleProject.as_view(), name="single_sub_project"),
    path('search/', views.SearchPage.as_view(), name="search"),
    path('search/promote', views.SearchPage.as_view(), name="promote"),
    path('search/inactivetoday', views.SearchPage.as_view(), name="inactivetoday"),
    path('search/inactive2month', views.SearchPage.as_view(), name="inactive2month"),
    path('search/latest_actived', views.SearchPage.as_view(), name="latest_actived"),
    path('search/without_files', views.SearchPage.as_view(), name="without_files"),
    path('search/has_note', views.SearchPage.as_view(), name="has_note"),
    path('search/less_than_20', views.SearchPage.as_view(), name="less_than_20"),
    path('search/more_than_80', views.SearchPage.as_view(), name="more_than_80"),
    path('search/without_gharardad', views.SearchPage.as_view(), name="without_gharardad"),
    path('search/week_end_date', views.SearchPage.as_view(), name="week_end_date"),
    path('search/month_end_date', views.SearchPage.as_view(), name="month_end_date"),
    path('search/month_end_date', views.SearchPage.as_view(), name="month_end_date"),
    path('search/object_type/<objt>', views.SearchPage.as_view(), name="object_type"),
]
