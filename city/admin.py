from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import *

# Register your models here.


class CityAdmin(ExportActionMixin, admin.ModelAdmin):

    list_display = ("city", "slug", "miangin_pishraft", "view_count")
    list_editable = ("slug", )
    list_filter = ("miangin_pishraft", )
    prepopulated_fields = {"slug": ("city",)}

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }


admin.site.register(CityProject, CityAdmin)
