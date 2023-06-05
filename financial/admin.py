from django.contrib import admin
from django.contrib.admin import TabularInline
from import_export.admin import ExportActionMixin
from financial.models import *

# Register your models here.


class StorageAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("StoreName", "StoreAdmin")
    raw_id_fields = ['StoreAdmin']
    list_filter = ("StoreAdmin", )


class InquiryInline(TabularInline):
    model = Inquiry
    # list_display = ("title", "course",)


class PropertyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("Commodity", "CommodityPrice", "BuyDateTime")
    raw_id_fields = ['Storage']
    list_filter = ("ForProject", "BuyDay", "Storage", )
    inlines = [InquiryInline]
    fieldsets = (
        ('اطلاعات خرید', {
            'fields': ('Status', 'Commodity', 'CommodityDesc', 'Storage', 'ForProject', 'Requester', ),
            'description': 'اطلاعات محصول را در اینجا وارد کنید',
        }),
        ('اطلاعات فروشگاه و محصول', {
            'fields': ('BuyFrom', 'CommodityPrice', 'Buyer', ),
            'classes': ('collapse', ),
        }),
        ('تصاویر و مستندات', {
            'fields': ('RequestPhoto', 'CommodityPhoto', 'BuyFactor', ),
            'classes': ('collapse', ),
        }),
    )


admin.site.register(Storage, StorageAdmin)
admin.site.register(PPP, PropertyAdmin)
