from django.dispatch import receiver
from django.db.models import Q
import accounts.models
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.db import models
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User, Group
from city.models import CityProject


def calculate_percent(kol, jozea):
    if kol == 0:
        return 0
    elif kol == jozea:
        return 100
    else:
        return int(jozea) * 100 / int(kol)


def validate_darsad(value):
    if value > 100:
        raise ValidationError('یک عدد کوچکتر از 100 وارد کتید')
    elif value < 0:
        raise ValidationError('یک عدد بزرگتر از 0 وارد کتید')


class MapObjectTypes(models.Model):
    title = models.CharField(max_length=202, verbose_name='عنوان شیع')
    icon = models.ImageField(upload_to='files/images/obj_icon', verbose_name='آیکون')
    marhalel_ejra_s = models.ManyToManyField('MaraheleEjra', verbose_name='مراحل اجرا')

    class Meta:
        verbose_name = "نوع پروژه"
        verbose_name_plural = "نوع پروژه"

    def __str__(self):
        return self.title

    def get_marahels(self):
        return self.marhalel_ejra_s.all().count()


class MaraheleEjra(models.Model):
    marhale = models.CharField(max_length=110, verbose_name='نام مرحله', null=False, blank=False)
    vahed = models.CharField(max_length=110, verbose_name='واحد', null=True, blank=True)

    class Meta:
        verbose_name = "مراحل اجرا"
        verbose_name_plural = "مراحل اجرا"

    def __str__(self):
        return self.marhale


class ProjectFiles(models.Model):
    DocChoices = (
        ('image', 'تصویر'),
        ('gharardad', 'قرارداد'),
        ('documents', 'مستندات'),
        ('file', 'فایل'),
        ('license', 'مجوز'),
        ('map', 'نقشه'),
    )
    DocName = models.CharField(max_length=110, verbose_name='توضیحات', null=False, blank=False)
    MDIIcon = models.CharField(verbose_name='آیکون', max_length=110, default="filter_drama",
                               help_text="نام آیکون را از <a href='https://materializecss.com/icons.html'>"
                                         "https://materializecss.com/icons.html</a> انتخاب کنید")
    photo = models.FileField(upload_to='files/images/project/sub', verbose_name='فایل', default="")
    DocType = models.CharField(default="image", max_length=72, choices=DocChoices, verbose_name="نوع فایل")
    Uploader = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, null=True,
                                 editable=False, verbose_name="آپلود کننده")
    UploadTime = models.DateTimeField(auto_now=True, blank=True, null=True, editable=False, verbose_name='زمان بارگزاری')

    class Meta:
        verbose_name = "فایلهای پروژه"
        verbose_name_plural = "فایل های پروژه"

    def __str__(self):
        return self.DocType + ":: " + self.DocName


def update_avg_city(related_city):
    hamshahri = Project.objects.filter(Q(RelatedCity__slug__contains=related_city.slug))
    miangin_pishrafte_project = 0
    miangin_pishrafte_project_count = 0

    for spd_temp in hamshahri:
        print("hamshahri: ", spd_temp.title, spd_temp.pishrafte_kol)
        miangin_pishrafte_project = miangin_pishrafte_project + spd_temp.pishrafte_kol
        miangin_pishrafte_project_count = miangin_pishrafte_project_count + 1

    if miangin_pishrafte_project == 0:
        related_city.miangin_pishraft = 0
    else:
        related_city.miangin_pishraft = miangin_pishrafte_project / miangin_pishrafte_project_count

    print(related_city.slug, related_city.miangin_pishraft)
    CityProject.objects.filter(Q(slug__contains=related_city.slug)).update(
        miangin_pishraft=related_city.miangin_pishraft
    )

    return related_city.miangin_pishraft


class Project(models.Model):
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name='عنوان')
    photo = models.ImageField(upload_to='files/images/project/sub', verbose_name='تصویر پروژه', default="")
    RelatedCity = models.ForeignKey(CityProject, blank=False, null=True, on_delete=models.CASCADE,
                                    verbose_name="شهر مربوطه")
    type = models.ForeignKey(MapObjectTypes, blank=False, null=False, on_delete=models.CASCADE,
                             verbose_name='نوع پروژه')
    pishrafte_kol = models.IntegerField(validators=[validate_darsad], editable=False, verbose_name='پیشرفت کل')
    date_start = jmodels.jDateField(verbose_name='تاریخ شروع')
    date_end = jmodels.jDateField(verbose_name='تاریخ پایان')
    team = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, verbose_name='سرپرست کارگاه')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    location = PlainLocationField(based_fields=['city'], zoom=10, null=True, suffix=['city'],
                                  verbose_name='موقعیت مکانی')
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True,
                                       editable=False, verbose_name='آخرین بروزرسانی')
    promote = models.BooleanField(default=False, verbose_name="پروژه ویژه")
    Documents = models.ManyToManyField(ProjectFiles, blank=True, verbose_name="مستندات و تصاویر")
    note = models.TextField(default="", verbose_name='یادداشت', blank=True, null=True)
    #
    marhale1 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 1')
    marhale1full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 1')
    marhale1accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 1')
    marhale2 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 2')
    marhale2full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 2')
    marhale2accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 2')
    marhale3 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 3')
    marhale3full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 3')
    marhale3accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 3')
    marhale4 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 4')
    marhale4full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 4')
    marhale4accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 4')
    marhale5 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 5')
    marhale5full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 5')
    marhale5accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 5')
    marhale6 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 6')
    marhale6full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 6')
    marhale6accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 6')
    marhale7 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 7')
    marhale7full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 7')
    marhale7accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 7')
    marhale8 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 8')
    marhale8full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 8')
    marhale8accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 8')
    marhale9 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 9')
    marhale9full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 9')
    marhale9accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 9')
    marhale10 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 10')
    marhale10full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 10')
    marhale10accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 10')
    marhale11 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 11')
    marhale11full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 11')
    marhale11accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 11')
    marhale12 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 12')
    marhale12full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 12')
    marhale12accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 12')
    marhale13 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 13')
    marhale13full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 13')
    marhale13accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 13')
    marhale14 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 14')
    marhale14full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 14')
    marhale14accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 14')
    marhale15 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 15')
    marhale15full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 15')
    marhale15accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 15')
    marhale16 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 16')
    marhale16full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 16')
    marhale16accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 16')
    marhale17 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 17')
    marhale17full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 17')
    marhale17accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 17')
    marhale18 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 18')
    marhale18full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 18')
    marhale18accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 18')
    marhale19 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 19')
    marhale19full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 19')
    marhale19accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 19')
    marhale20 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 20')
    marhale20full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 20')
    marhale20accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 20')
    marhale21 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 21')
    marhale21full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 21')
    marhale21accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 21')
    marhale22 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 22')
    marhale22full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 22')
    marhale22accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 22')
    marhale23 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 23')
    marhale23full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 23')
    marhale23accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 23')
    marhale24 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 24')
    marhale24full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 24')
    marhale24accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 24')
    marhale25 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 25')
    marhale25full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 25')
    marhale25accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 25')
    marhale26 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 26')
    marhale26full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 26')
    marhale26accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 26')
    marhale27 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 27')
    marhale27full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 27')
    marhale27accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 27')
    marhale28 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 28')
    marhale28full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 28')
    marhale28accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 28')
    marhale29 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 29')
    marhale29full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 29')
    marhale29accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 29')
    marhale30 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='توضیحات مرحله 30')
    marhale30full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 30')
    marhale30accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 30')

    def save(self, *args, **kwargs):
        real_miangin_all = 0
        real_miangin_count = 0
        for i in range(1, 30):
            m_f = "marhale%sfull" % i
            m_a = "marhale%saccomplished" % i
            if self.__getattribute__(m_a).numerator > 0:
                real_miangin_all = real_miangin_all + calculate_percent(self.__getattribute__(m_f).numerator,
                                                                        self.__getattribute__(m_a).numerator)
                real_miangin_count = real_miangin_count + 1

        if real_miangin_all == 0:
            self.pishrafte_kol = 0
        else:
            self.pishrafte_kol = real_miangin_all / real_miangin_count

        update_avg_city(self.RelatedCity)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "پروژه ها"
        verbose_name_plural = "پروژه"

    def __str__(self):
        return self.title

    @property
    def thumbnail_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" style="object-fit:contain; height:auto; max-height:110px; " width="110" />'.format(
                    self.photo.url))
        return ""


@receiver(models.signals.post_save, sender=Project)
def proj_save(sender, instance, created, **kwargs):
    update_avg_city(instance.RelatedCity)
    print('post save callback')
