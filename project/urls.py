from django.conf import Settings, settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('project/',            views.project.as_view(), name="project"),
    path('project/<slug>',      views.single_project.as_view(), name="single_project"),
    path('project/<slug>/<id>', views.single_sub_project.as_view(), name="single_sub_project"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
