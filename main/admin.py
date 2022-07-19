from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
# from .models import project
from .models import *

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


class ProjectAdmin(admin.ModelAdmin):
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('https://cdn.jsdelivr.net/gh/rastikerdar/sahel-font@v3.4.0/dist/font-face.css','css/font.css'),
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )

class SubProjectAdmin(admin.ModelAdmin):
    class Media:
        # js = ('js/admin/my_own_admin.js',)
        css = {
             'all': ('https://cdn.jsdelivr.net/gh/rastikerdar/sahel-font@v3.4.0/dist/font-face.css','css/font.css')
        }
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(project,ProjectAdmin)
admin.site.register(subproject,SubProjectAdmin)
admin.site.register(MapObjectTypes)
admin.site.register(MaraheleEjra)
