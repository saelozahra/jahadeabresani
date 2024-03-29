from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from .models import *
from inline_ordering.admin import OrderableStackedInline
# you need import this for adding jalali calander widget


@admin.register(MapObjectTypes)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ("title", "icon")


class MaraheleEjraAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("marhale", "vahed")


class MapObjectTypesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "get_marahels")


class MarhaleInline(OrderableStackedInline):
    model = MaraheleEjra
    # list_display = ("title", "course",)


class ProjectAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "team", "pishrafte_kol", "thumbnail_preview", "view_count")
    raw_id_fields = ['team']
    readonly_fields = ('thumbnail_preview',)
    inlines = [MarhaleInline]
    fieldsets = (
        ('اطلاعات پروژه', {
            'fields': ('title', 'type', 'money', 'team', 'promote', ),
            'description': 'اطلاعات پروژه را در اینجا وارد کنید',
        }),
        ('ددلاین', {
            'fields': ('date_start', 'date_end', ),
            'classes': ('collapse', ),
        }),
        ('نشانی', {
            'fields': ('RelatedCity', 'location', ),
            'classes': ('collapse', ),
        }),
        ('مستندات', {
            'fields': ('photo', 'Documents', 'note', ),
            'classes': ('collapse', 'mostanadat', ),
        }),
    )

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview
    thumbnail_preview.short_description = 'تصویر پروژه'
    thumbnail_preview.allow_tags = True

    class Media:
        js = ('js/admin_scripts.js',)
        css = {
             'all': ('css/adminstyle.css',),
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFiles)
admin.site.register(MaraheleEjra, MaraheleEjraAdmin)
