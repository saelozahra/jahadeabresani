from django.urls import path
from . import views
urlpatterns = [
    # path(r'^api/project$', views.ApiSaveProjectNote.as_view(), name="api_save_project_note"),
    path('api/project/', views.ApiSaveProjectNote.as_view(), name="api_save_project_note"),
]

