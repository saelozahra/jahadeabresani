from datetime import datetime

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
    location = PlainLocationField(based_fields=['city'], zoom=8, suffix=['city'], verbose_name='موقعیت مکانی')
    date_start = jmodels.jDateField(verbose_name='تاریخ شروع پروژه')
    date_end = jmodels.jDateField(verbose_name='تاریخ پایان پروژه')
    miangin_pishraft = models.IntegerField(default=0, editable=False, verbose_name='میانگین پیشرفت کل')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    #
    mojavez = models.FileField(upload_to='files/images/project/mojavez', verbose_name='مجوزهای پروژه', default="")
    mostanadat = models.FileField(upload_to='files/images/project/mostanadat', verbose_name='مستندات پروژه', default="")
    file_ha = models.FileField(upload_to='files/images/project', verbose_name='فایلهای پروژه', default="")
    #
    note    = models.TextField(default="" ,verbose_name='یادداشت' )
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
    marhale1percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 1')
    marhale2 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 2')
    marhale2percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 2')
    marhale3 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 3')
    marhale3percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 3')
    marhale4 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 4')
    marhale4percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 4')
    marhale5 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 5')
    marhale5percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 5')
    marhale6 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 6')
    marhale6percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 6')
    marhale7 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 7')
    marhale7percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 7')
    marhale8 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 8')
    marhale8percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 8')
    marhale9 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 9')
    marhale9percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 9')
    marhale10 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 10')
    marhale10percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 10')
    marhale11 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 11')
    marhale11percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 11')
    marhale12 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 12')
    marhale12percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 12')
    marhale13 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 13')
    marhale13percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 13')
    marhale14 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 14')
    marhale14percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 14')
    marhale15 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 15')
    marhale15percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 15')
    marhale16 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 16')
    marhale16percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 16')
    marhale17 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 17')
    marhale17percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 17')
    marhale18 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 18')
    marhale18percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 18')
    marhale19 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 19')
    marhale19percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 19')
    marhale20 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 20')
    marhale20percent = models.IntegerField( default="0", verbose_name='درصد پیشرفت مرحله 20')

    class Meta:
        verbose_name = "زیرپروژه ها"
        verbose_name_plural = "زیرپروژه"

    def __str__(self):
        return self.title
