from django.contrib import admin
from django.utils.safestring import mark_safe
from django_jalali.admin.filters import JDateFieldListFilter
# from .models import project
import main.models
from .models import *

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


class ProjectAdmin(admin.ModelAdmin):

    list_display = ("title", "city", "miangin_pishraft", "thumbnail_preview", "view_count")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        # ('city', main.models.project.city),
    )

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'تصویر پروژه'
    thumbnail_preview.allow_tags = True


class SubProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "photo", "pishrafte_kol", "view_count")
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('https://cdn.jsdelivr.net/gh/rastikerdar/sahel-font@v3.4.0/dist/font-face.css','css/font.css')
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(SubProject, SubProjectAdmin)
admin.site.register(MapObjectTypes)
admin.site.register(MaraheleEjra)
