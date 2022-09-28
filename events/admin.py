from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import *

# Register your models here.


class EventsAdmin(ExportActionMixin, admin.ModelAdmin):

    list_display = ("RelatedProject", "OwnerUser", "EventType", "day")
    list_filter = ("RelatedProject", "OwnerUser", )


admin.site.register(Events, EventsAdmin)
