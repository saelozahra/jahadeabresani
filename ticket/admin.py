from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *
import django_jalali.admin as jadmin

# Register your models here.


class TicketMessageAdmin(admin.ModelAdmin):
    list_filter = (
        ('jdate_tarikh', JDateFieldListFilter),
    )


# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketMessage, TicketMessageAdmin)
admin.site.register(Department)
