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


class Inquiry(models.Model):
    StoreName = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=False, blank=False)
    StoreAddress = models.TextField(verbose_name='آدرس', null=True, blank=True)
    StoreLocation = PlainLocationField(based_fields=['city'], zoom=10, null=True, suffix=['StoreAddress'],
                                       verbose_name='موقعیت مکانی')
    StoreAdmin = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True,
                                   verbose_name="انبار دار")

    class Meta:
        verbose_name = "استعلام"
        verbose_name_plural = "استعلام"

    def __str__(self):
        return "انبار" + self.StoreName


class PPP(models.Model):
    # ProductPurchaseProcess
    StatusChoices = (
        (1, '  1️⃣ بارگزاری'),
        (2, ' 2️⃣ تائید ناظر'),
        (3, ' 3️⃣ استعلام'),
        (4, ' 4️⃣ دستور خرید'),
        (5, '5️⃣ اخذ پیش فاکتور '),
        (6, '6️⃣ واریز وجه'),
        (7, '7️⃣ صدور فاکتور'),
        (8, '8️⃣ ارسال کالا از کارخانه'),
        (9, '9️⃣ ورود کالا به انبار'),
        (10, '🔟 تحویل به مجری'),
        (11, '🔢 نصب قطعه'),
    )
    Status = models.SmallIntegerField(verbose_name="وضعیت", default=1, choices=StatusChoices)
    Commodity = models.CharField(max_length=110, verbose_name='محصول', null=False, blank=False)
    CommodityVolume = models.CharField(max_length=1313, verbose_name='میزان کالا', null=True, blank=True)
    CommodityDesc = models.TextField(verbose_name='توضیحات', null=True, blank=True, help_text="توضیحات یا نوع محصول")
    CommodityPrice = models.IntegerField(verbose_name='قیمت', null=True, blank=True, help_text="قیمت به تومان")
    CommodityPhoto = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر محصول')
    ####
    BuyFrom = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=True, blank=True)
    Buyer = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True, related_name="buyer", verbose_name="خریدار")
    Storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="انبار")
    ForProject = models.ForeignKey(main.models.Project, on_delete=models.CASCADE, null=False, verbose_name="پروژه مربوطه")
    BuyFactor = models.ImageField(upload_to='files/finance/factor', verbose_name='تصویر فاکتور خرید')
    ####
    RequestPhoto = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر نامه درخواست')
    Requester = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=False, default="",
                                  blank=True, related_name="requester", verbose_name="درخواست دهنده")
    BuyDay = jmodels.jDateField(editable=False, auto_now_add=True, verbose_name='روز خرید')
    BuyDateTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان خرید')

    class Meta:
        verbose_name = "پروسه خرید محصول"
        verbose_name_plural = "خرید محصول"

    def __str__(self):
        return self.Commodity
