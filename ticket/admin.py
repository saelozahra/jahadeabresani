from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *
import django_jalali.admin as jadmin

# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ("User1", "User2", "Zaman", "Lead")


# class ChatMessageAdmin(admin.ModelAdmin):
#     # list_display = ("RelatedChat", "Sender", "Text")
#
#     def save_model(self, request, obj, form, change):
#         if getattr(obj, 'Sender', None) is None:
#             obj.Sender = request.user
#         obj.save()
# @TODO: save chat

admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage)
admin.site.register(Department)
