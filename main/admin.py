from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin, ImportExportActionModelAdmin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


@admin.register(MapObjectTypes)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ("title", "icon")
    pass


class ProjectAdmin(ExportActionMixin, admin.ModelAdmin):

    list_display = ("city", "miangin_pishraft", "view_count")
    prepopulated_fields = {"slug": ("city",)}

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }


class MaraheleEjraAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("marhale", "vahed")


class MapObjectTypesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "get_marahels")


class SubProjectAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "team", "photo", "pishrafte_kol", "thumbnail_preview", "view_count")

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview
    thumbnail_preview.short_description = 'تصویر پروژه'
    thumbnail_preview.allow_tags = True

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(CityProject, ProjectAdmin)
admin.site.register(Project, SubProjectAdmin)
admin.site.register(ProjectFiles)
admin.site.register(MaraheleEjra, MaraheleEjraAdmin)
