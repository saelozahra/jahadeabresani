from django.contrib import admin
from import_export.admin import ExportActionMixin
from financial.models import Storage

# Register your models here.


class StorageAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("StoreName", "StoreAdmin")
    raw_id_fields = ['StoreAdmin']
    readonly_fields = ('thumbnail_preview',)


admin.site.register(Storage, StorageAdmin)
