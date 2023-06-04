from django.urls import path
from . import views
urlpatterns = [
    path('api/city/', views.ApiSaveCityNote.as_view(), name="api_save_project_note"),
    path('api/project/', views.ApiUpdateProject.as_view(), name="api_save_project_note"),
    path('api/project/type/<pt_id>', views.ApiProjectType.as_view(), name="api_project_type"),
    path('api/project/mosatanadat/<pt_id>', views.ApiProjectMosatanadat.as_view(), name="api_project_type"),
    path('api/financial/', views.ApiFinance.as_view(), name="api_finance"),
]

