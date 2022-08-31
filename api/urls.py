from django.urls import path
from . import views
urlpatterns = [
    path('api/project/', views.ApiSaveProjectNote.as_view(), name="api_save_project_note"),
    path('api/project/type/<pt_id>', views.ApiProjectType.as_view(), name="api_project_type"),
]

