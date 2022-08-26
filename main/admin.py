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

    list_display = ("title", "city", "miangin_pishraft", "thumbnail_preview", "view_count")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }
    thumbnail_preview.short_description = 'تصویر پروژه'
    thumbnail_preview.allow_tags = True


class MaraheleEjraAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("marhale", "vahed")


class MapObjectTypesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "get_marahels")


class SubProjectAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "team", "photo", "pishrafte_kol", "view_count")

    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(SubProject, SubProjectAdmin)
# admin.site.register(MapObjectTypes, MapObjectTypesAdmin)
admin.site.register(MaraheleEjra, MaraheleEjraAdmin)
