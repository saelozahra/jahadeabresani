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


class RequestTicket(models.Model):
    Commodity = models.CharField(max_length=110, verbose_name='نام کالا', null=False, blank=False)
    CommodityVolume = models.CharField(max_length=1313, verbose_name='میزان کالا', null=True, blank=True)
    CommodityDesc = models.TextField(verbose_name='توضیحات', null=True, blank=True, help_text="توضیحات")
    Photo = models.ImageField(upload_to='files/finance', verbose_name='تصویر نامه درخواست')
    Requester = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=False, verbose_name="درخواست دهنده")
    BuyDay = jmodels.jDateField(editable=False, auto_now_add=True, verbose_name='روز درخواست')
    BuyDateTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان درخواست')
    ForProject=models.ForeignKey(main.models.Project, on_delete=models.CASCADE, null=False, verbose_name="پروژه مربوطه")

    def save(self, *args, **kwargs):
        PPP.objects.create(
            Commodity=self.Commodity,
            CommodityDesc=self.CommodityDesc,
            ForProject=self.ForProject
        )

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "نامه درخواست"
        verbose_name_plural = "نامه درخواست"

    def __str__(self):
        return self.CommodityVolume, " «", self.Commodity, "»"


class PPP(models.Model):
    # ProductPurchaseProcess
    Commodity = models.CharField(max_length=110, verbose_name='محصول', null=False, blank=False)
    CommodityDesc = models.TextField(verbose_name='توضیحات', null=True, blank=True, help_text="توضیحات یا نوع محصول")
    CommodityPrice = models.IntegerField(verbose_name='قیمت', null=True, blank=True, help_text="قیمت به تومان")
    BuyFrom = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=True, blank=True)
    Buyer = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True, verbose_name="خریدار")
    Storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="انبار")
    BuyDay = jmodels.jDateField(editable=False, auto_now_add=True, verbose_name='روز خرید')
    BuyDateTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان خرید')
    ForProject=models.ForeignKey(main.models.Project, on_delete=models.CASCADE, null=False, verbose_name="پروژه مربوطه")
    Photo = models.ImageField(upload_to='files/finance', verbose_name='تصویر محصول')
    BuyFactor = models.ImageField(upload_to='files/finance/factor', verbose_name='تصویر فاکتور خرید')
    ####
    RequestTicket = models.ForeignKey(RequestTicket, on_delete=models.CASCADE, blank=False, null=False, verbose_name="نامه درخواست")

    class Meta:
        verbose_name = "پروسه خرید محصول"
        verbose_name_plural = "پروسه خرید محصول"

    def __str__(self):
        return self.Commodity
