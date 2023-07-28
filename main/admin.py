from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from .models import *
# you need import this for adding jalali calander widget


@admin.register(MapObjectTypes)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ("title", "icon")


class MaraheleEjraAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("marhale", "vahed")


class MapObjectTypesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "get_marahels")


class ProjectAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("title", "team", "pishrafte_kol", "thumbnail_preview", "view_count")
    raw_id_fields = ['team']
    readonly_fields = ('thumbnail_preview',)
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
        ('مراحل اجرا', {
            'fields': (
                        'marhale1', 'marhale1full', 'marhale1accomplished',
                        'marhale2', 'marhale2full', 'marhale2accomplished',
                        'marhale3', 'marhale3full', 'marhale3accomplished',
                        'marhale4', 'marhale4full', 'marhale4accomplished',
                        'marhale5', 'marhale5full', 'marhale5accomplished',
                        'marhale6', 'marhale6full', 'marhale6accomplished',
                        'marhale7', 'marhale7full', 'marhale7accomplished',
                        'marhale8', 'marhale8full', 'marhale8accomplished',
                        'marhale9', 'marhale9full', 'marhale9accomplished',
                        'marhale10', 'marhale10full', 'marhale10accomplished',
                        'marhale11', 'marhale11full', 'marhale11accomplished',
                        'marhale12', 'marhale12full', 'marhale12accomplished',
                        'marhale13', 'marhale13full', 'marhale13accomplished',
                        'marhale14', 'marhale14full', 'marhale14accomplished',
                        'marhale15', 'marhale15full', 'marhale15accomplished',
                        'marhale16', 'marhale16full', 'marhale16accomplished',
                        'marhale17', 'marhale17full', 'marhale17accomplished',
                        'marhale18', 'marhale18full', 'marhale18accomplished',
                        'marhale19', 'marhale19full', 'marhale19accomplished',
                        'marhale20', 'marhale20full', 'marhale20accomplished',
                        'marhale21', 'marhale21full', 'marhale21accomplished',
                        'marhale22', 'marhale22full', 'marhale22accomplished',
                        'marhale23', 'marhale23full', 'marhale23accomplished',
                        'marhale24', 'marhale24full', 'marhale24accomplished',
                        'marhale25', 'marhale25full', 'marhale25accomplished',
                        'marhale26', 'marhale26full', 'marhale26accomplished',
                        'marhale27', 'marhale27full', 'marhale27accomplished',
                        'marhale28', 'marhale28full', 'marhale28accomplished',
                        'marhale29', 'marhale29full', 'marhale29accomplished',
                        'marhale30', 'marhale30full', 'marhale30accomplished',
                       ),
            'classes': ('marahel', ),
            'description': 'مراحل اجرای پروژه',
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
