from django.urls import path
from . import views
urlpatterns = [
    path('city/<slug>', views.SingleCity.as_view(), name="SingleCity"),
]
