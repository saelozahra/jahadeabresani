from django.core.exceptions import ValidationError
from django_jalali.db.models import jDateTimeField
from django.db import models
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User, Group


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


class MaraheleEjra(models.Model):
    marhale = models.CharField(max_length=110, verbose_name='مرحله')

    class Meta:
        verbose_name = "مراحل اجرا"
        verbose_name_plural = "مراحل اجرا"

    def __str__(self):
        return self.marhale


class project(models.Model):
    objects = jmodels.jManager()
    title = models.CharField(max_length=202, verbose_name='عنوان')
    slug = models.SlugField(default=title, unique=True, verbose_name='نشانی')
    photo = models.ImageField(upload_to='files/images/project', verbose_name='تصویر پروژه', default="")
    city = models.CharField(max_length=202, verbose_name='شهر')
    location = PlainLocationField(based_fields=['city'], zoom=4, suffix=['city'], verbose_name='موقعیت مکانی')
    date_start = jmodels.jDateField(verbose_name='تاریخ شروع پروژه', blank=True, null=True)
    date_end = jmodels.jDateField(verbose_name='تاریخ پایان پروژه', blank=True, null=True)
    miangin_pishraft = models.IntegerField(default=0, editable=False, verbose_name='میانگین پیشرفت کل')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    #
    mojavez = models.FileField(upload_to='files/images/project/mojavez', blank=True, null=True,
                               verbose_name='مجوزهای پروژه', default="")
    mostanadat = models.FileField(upload_to='files/images/project/mostanadat', blank=True, null=True,
                                  verbose_name='مستندات پروژه', default="")
    file_ha = models.FileField(upload_to='files/images/project', blank=True, null=True, verbose_name='فایلهای پروژه',
                               default="")
    #
    note = models.TextField(default="", verbose_name='یادداشت', blank=True, null=True)

    #
    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه"

    def __str__(self):
        return self.title

    def jdate_end(self):
        return self.date_end


class subproject(models.Model):
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name='عنوان')
    photo = models.ImageField(upload_to='files/images/project/sub', verbose_name='تصویر زیرپروژه', default="")
    project_id = models.ForeignKey(project, blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="پروژه مربوطه")
    type = models.ForeignKey(MapObjectTypes, blank=False, null=False, on_delete=models.CASCADE,
                             verbose_name='نوع پروژه')
    pishrafte_kol = models.IntegerField(validators=[validate_darsad], verbose_name='پیشرفت کل')
    date_start = jmodels.jDateField(verbose_name='تاریخ شروع')
    date_end = jmodels.jDateField(verbose_name='تاریخ پایان')
    team = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مدیر پروژه')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    #
    naghshe = models.FileField(upload_to='files/images/subproject/naghshe', blank=True, null=True,
                               verbose_name='نقشه اجرا', default="")
    mojavez = models.FileField(upload_to='files/images/subproject/mojavez', blank=True, null=True,
                               verbose_name='مجوزهای پروژه', default="")
    mostanadat = models.FileField(upload_to='files/images/subproject/mostanadat', blank=True, null=True,
                                  verbose_name='مستندات پروژه', default="")
    file_ha = models.FileField(upload_to='files/images/subproject', blank=True, null=True, verbose_name='فایلهای پروژه',
                               default="")
    #
    marhale1 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 1')
    marhale1full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 1')
    marhale1accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 1')
    marhale2 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 2')
    marhale2full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 2')
    marhale2accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 2')
    marhale3 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 3')
    marhale3full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 3')
    marhale3accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 3')
    marhale4 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 4')
    marhale4full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 4')
    marhale4accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 4')
    marhale5 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 5')
    marhale5full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 5')
    marhale5accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 5')
    marhale6 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 6')
    marhale6full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 6')
    marhale6accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 6')
    marhale7 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 7')
    marhale7full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 7')
    marhale7accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 7')
    marhale8 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 8')
    marhale8full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 8')
    marhale8accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 8')
    marhale9 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 9')
    marhale9full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 9')
    marhale9accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 9')
    marhale10 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 10')
    marhale10full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 10')
    marhale10accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 10')
    marhale11 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 11')
    marhale11full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 11')
    marhale11accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 11')
    marhale12 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 12')
    marhale12full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 12')
    marhale12accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 12')
    marhale13 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 13')
    marhale13full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 13')
    marhale13accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 13')
    marhale14 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 14')
    marhale14full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 14')
    marhale14accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 14')
    marhale15 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 15')
    marhale15full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 15')
    marhale15accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 15')
    marhale16 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 16')
    marhale16full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 16')
    marhale16accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 16')
    marhale17 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 17')
    marhale17full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 17')
    marhale17accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 17')
    marhale18 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 18')
    marhale18full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 18')
    marhale18accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 18')
    marhale19 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 19')
    marhale19full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 19')
    marhale19accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 19')
    marhale20 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 20')
    marhale20full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 20')
    marhale20accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 20')

    class Meta:
        verbose_name = "زیرپروژه ها"
        verbose_name_plural = "زیرپروژه"

    def __str__(self):
        return self.title
