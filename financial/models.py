from django.db import models
from location_field.models.plain import PlainLocationField
from django_jalali.db import models as jmodels
import main.models
import accounts.models
# Create your models here.


class Storage(models.Model):
    StoreName = models.CharField(max_length=110, verbose_name='نام انبار', null=False, blank=False)
    StoreAddress = models.TextField(verbose_name='آدرس', null=True, blank=True)
    StoreLocation = PlainLocationField(based_fields=['city'], zoom=10, null=True, suffix=['StoreAddress'],
                                       verbose_name='موقعیت مکانی')
    StoreAdmin = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True,
                                   verbose_name="انبار دار")

    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبار"

    def __str__(self):
        return "انبار" + self.StoreName


class Property(models.Model):
    Commodity = models.CharField(max_length=110, verbose_name='محصول', null=False, blank=False)
    CommodityDesc = models.TextField(verbose_name='توضیحات', null=True, blank=True, help_text="توضیحات یا نوع محصول")
    CommodityPrice = models.IntegerField(verbose_name='قیمت', null=True, blank=True, help_text="قیمت به تومان")
    BuyFrom = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=False, blank=False)
    Buyer = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=False, verbose_name="خریدار")
    Storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=False, blank=False, verbose_name="انبار")
    BuyDay = jmodels.jDateField(editable=False, auto_now_add=True, verbose_name='روز خرید')
    BuyDateTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان خرید')
    ForProject=models.ForeignKey(main.models.Project, on_delete=models.CASCADE, null=False, verbose_name="پروژه مربوطه")
    Photo = models.ImageField(upload_to='files/finance', verbose_name='تصویر محصول')
    BuyFactor = models.ImageField(upload_to='files/finance/factor', verbose_name='تصویر فاکتور خرید')

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول"

    def __str__(self):
        return self.Commodity
