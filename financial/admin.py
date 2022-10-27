from django.contrib import admin
from import_export.admin import ExportActionMixin
from financial.models import *

# Register your models here.


class StorageAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("StoreName", "StoreAdmin")
    raw_id_fields = ['StoreAdmin']
    list_filter = ("StoreAdmin", )


class PropertyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("Commodity", "CommodityPrice", "BuyFrom", "BuyDateTime")
    raw_id_fields = ['Storage']
    list_filter = ("ForProject", "BuyDay", "Storage", )
    fieldsets = (
        ('اطلاعات خرید', {
            'fields': ('Commodity', 'CommodityDesc', 'Storage', 'Buyer', 'ForProject', ),
            'description': 'اطلاعات محصول را در اینجا وارد کنید',
        }),
        ('اطلاعات فروشگاه و محصول', {
            'fields': ('BuyFrom', 'CommodityPrice', ),
            'classes': ('collapse', ),
        }),
        ('تصاویر و مستندات', {
            'fields': ('Photo', 'BuyFactor', ),
            'classes': ('collapse', ),
        }),
    )


admin.site.register(Storage, StorageAdmin)
admin.site.register(Property, PropertyAdmin)
