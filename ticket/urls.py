from django.urls import path
from . import views
urlpatterns = [
    path('ticket/',     views.Tickets.as_view(), name="tickets"),
    path('ticket/<id>', views.SingleTicket.as_view(), name="SingleTicket"),
]