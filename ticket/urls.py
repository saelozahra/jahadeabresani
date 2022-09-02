from django.urls import path
from . import views
urlpatterns = [
    path('chat/', views.ChatList.as_view(), name="ChatList"),
    path('chat/<chat_id>', views.ChatList.as_view(), name="ShowSingleChat"),
    path('chat/<my_slug>/<to_slug>', views.CreateNewChat.as_view(), name="CreateNewChat"),
]