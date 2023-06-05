from django.db import models
from location_field.models.plain import PlainLocationField
from django_jalali.db import models as jmodels

from events.models import Events
import main.models
import accounts.models
# Create your models here.


class Aghlam(models.Model):
    Name = models.CharField(max_length=313, verbose_name='نام انبار', null=False, blank=False)
    Volume = models.TextField(verbose_name='میزان', null=True, blank=True)
    Description = models.TextField(null=True, verbose_name='توضیحات')
    Storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, verbose_name="انبار")

    class Meta:
        verbose_name = "اقلام"
        verbose_name_plural = "اقلام"

    def __str__(self):
        return self.Name


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


class Pay(models.Model):
    PayType = (
        (1, '💴 نقدی 💵'),
        (2, '🏧 اقساط'),
    )
    Status = models.PositiveSmallIntegerField(verbose_name="نوع پرداخت", default=1, choices=PayType)
    Amount = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ واریز شده", help_text="قیمت به تومان")
    #####
    BuyFrom = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=True, blank=True)
    HesabName = models.CharField(max_length=110, verbose_name='نام صاحب حساب', null=True, blank=True)
    ShopHesab = models.CharField(max_length=16, verbose_name='شماره کارت فروشنده', null=True, blank=True)
    ShopShaba = models.CharField(max_length=110, verbose_name='شماره شبای فروشنده', null=True, blank=True)
    ######
    Tarikh = models.DateTimeField(verbose_name='تاریخ واریز', blank=True)
    HesabMabda = models.TextField(max_length=110, verbose_name='حساب مبداء', null=True, blank=True)
    Sanad = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='پیوست سند')

    class Meta:
        verbose_name = "واریز"
        verbose_name_plural = "واریز"

    def __str__(self):
        return f"پرداخت {self.Amount} به {self.BuyFrom} "


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
    __original_status = None
    Commodity = models.CharField(max_length=110, verbose_name='محصول', null=False, blank=False)
    CommodityVolume = models.CharField(max_length=1313, verbose_name='میزان کالا', null=True, blank=True)
    CommodityDesc = models.TextField(verbose_name='توضیحات', null=True, blank=True, help_text="توضیحات یا نوع محصول")
    CommodityPrice = models.IntegerField(verbose_name='قیمت', null=True, blank=True, help_text="قیمت به تومان")
    CommodityPhoto = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر محصول')
    ########
    BuyFrom = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=True, blank=True)
    Buyer = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True, related_name="buyer", verbose_name="خریدار")
    Storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="انبار")
    ForProject = models.ForeignKey(main.models.Project, on_delete=models.CASCADE, null=False, verbose_name="پروژه مربوطه")
    BuyFactor = models.ImageField(upload_to='files/finance/factor', verbose_name='تصویر فاکتور خرید')
    PreFactor = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر پیش فاکتور')
    ####
    RequestPhoto = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر نامه درخواست')
    Requester = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=False, default="",
                                  blank=True, related_name="requester", verbose_name="درخواست دهنده")
    BuyDay = jmodels.jDateField(editable=False, auto_now_add=True, verbose_name='روز ثبت درخواست')
    BuyDateTime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان خرید')

    Pay = models.ForeignKey(Pay, on_delete=models.DO_NOTHING, null=True, blank=True, default="", verbose_name="پرداخت")

    class Meta:
        verbose_name = "پروسه خرید محصول"
        verbose_name_plural = "خرید محصول"

    def __str__(self):
        return self.Commodity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.Status

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        print("status: ", self.Status, self.__original_status)
        if self.Status != self.__original_status:
            if self.Status == 2:
                Events.objects.create(
                    EventType="تائید ناظر",
                    description="ناظر سازمان، این سفارش را تائید کرد",
                    OwnerUser=self.Requester,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 3:
                # @todo: اطلاعات استعلام
                Events.objects.create(
                    EventType="استعلام",
                    description=f"یک استعلام قیمت جدید برای {self.Commodity} ثبت شد",
                    OwnerUser=self.Buyer,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 4:
                Events.objects.create(
                    EventType="دستور خرید",
                    description=f"دستور خرید {self.Commodity} صادر شد",
                    OwnerUser=self.Buyer,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 5:
                Events.objects.create(
                    EventType="پیش فاکتور",
                    description="پیش فاکتور های درخواست شده در سامانه ثبت شدند",
                    OwnerUser=self.Buyer,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 6:
                Events.objects.create(
                    EventType="واریز وجه",
                    description=f"وجه پیش فاکتور تائید شده به حساب {self.BuyFrom} واریز شد",
                    OwnerUser=self.Buyer,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 7:
                Events.objects.create(
                    EventType="صدور فاکتور",
                    description=f"فاکتورهای نهائی {self.Commodity} صادر و بارگزاری شدند",
                    OwnerUser=self.Requester,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 8:
                Events.objects.create(
                    EventType="ارسال از کارخانه",
                    description=f"{self.Commodity} خریداری شده از کارخانه به سمت انبار {self.Storage} ارسال شد",
                    OwnerUser=self.Requester,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 9:
                Events.objects.create(
                    EventType="ورود به انبار",
                    description=f"{self.Commodity} خریداری شده به انبار {self.Storage}  تحویل داده شد",
                    OwnerUser=self.Requester,
                    RelatedProject=self.ForProject,
                )
            elif self.Status == 10:
                Events.objects.create(
                    EventType="تحویل به مجری",
                    description=f"محصول خریداری شده از انبار {self.Storage}   به {self.ForProject.team.get_full_name()} تحویل داده شد ",
                    OwnerUser=self.Requester,
                    RelatedProject=self.ForProject,
                )

        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_name = self.Status


class PurchaseOrder(models.Model):
    Orderer = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=False, default="",
                                blank=True, related_name="orderer", verbose_name="دستور دهنده")
    PurchaseTime = models.DateTimeField(auto_now=True, verbose_name="تاریخ ثبت")
    PurchaseOrderTicket = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True,
                                            verbose_name='تصویر نامه دستور خرید')
    ForProject = models.ForeignKey(main.models.Project, on_delete=models.DO_NOTHING, null=True, blank=True, default="",
                                   verbose_name="دستور خرید نسبت به استعلام")

    class Meta:
        verbose_name = "دستور خرید"
        verbose_name_plural = "دستور خرید"

    def __str__(self):
        return f"دستور خرید شماره {self.id} توسط {self.Orderer}"

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # @todo چک کن ببین تکراری نباشه
        Events.objects.create(
            EventType="اعلام دستور خرید",
            description=self.__str__(),
            OwnerUser=self.Orderer,
            RelatedProject=self.ForProject,
        )

        super().save(force_insert, force_update, *args, **kwargs)


class Inquiry(models.Model):
    Amount = models.PositiveBigIntegerField(default=0, verbose_name="قیمت", help_text="قیمت به تومان")
    StoreName = models.CharField(max_length=110, verbose_name='نام فروشگاه', null=False, blank=False)
    StoreAddress = models.TextField(max_length=313, verbose_name='آدرس', null=True, blank=True)
    StoreLocation = PlainLocationField(based_fields=['city'], zoom=10, null=True, suffix=['StoreAddress'],
                                       verbose_name='موقعیت مکانی')
    InquiryPhoto = models.ImageField(upload_to='files/finance/%Y/%m/%d/', blank=True, verbose_name='تصویر محصول')
    ProductPurchaseProcess = models.ForeignKey(PPP, on_delete=models.CASCADE, null=True, blank=True, default="", verbose_name="استعلام قیمت")

    PurchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True, default="",
                                verbose_name="ثبت دستور خرید")

    class Meta:
        verbose_name = "استعلام"
        verbose_name_plural = "استعلام"

    def __str__(self):
        return "انبار" + self.StoreName
