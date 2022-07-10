from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
# from .models import project
from .models import *

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


class ProjectAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )

class SubProjectAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_end', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(project,ProjectAdmin)
admin.site.register(subproject,SubProjectAdmin)
admin.site.register(MapObjectTypes)
admin.site.register(MaraheleEjra)
