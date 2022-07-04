from datetime import datetime

from django.core.exceptions import ValidationError
from django_jalali.db.models import jDateTimeField
from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User, Group


def validate_darsad(value):
    if value > 100:
        raise ValidationError('یک عدد کوچکتر از 100 وارد کتید')
    elif value < 0:
        raise ValidationError('یک عدد بزرگتر از 0 وارد کتید')


class map_object_types(models.Model):
        title = models.CharField(max_length=202, verbose_name='عنوان شیع')
        icon  = models.ImageField(upload_to='files/images/obj_icon',verbose_name='آیکون')
        marhalel_ejra_s = models.ManyToManyField('marhalel_ejra')
        class Meta:
            verbose_name = "نوع پروژه"
            verbose_name_plural = "نوع پروژه"
        def __str__(self):
            return self.title

class marhalel_ejra(models.Model):
    marhale = models.CharField(max_length=110, verbose_name='مرحله')
    class Meta:
        verbose_name = "مراحل اجرا"
        verbose_name_plural = "مراحل اجرا"
    def __str__(self):
        return self.marhale



class project(models.Model):
    title       = models.CharField(max_length=202, verbose_name='عنوان')
    slug        = models.SlugField(default=title,unique=True,verbose_name='نشانی')
    photo       = models.ImageField(upload_to='files/images/project',verbose_name='تصویر پروژه', default="")
    city        = models.CharField(max_length=202, verbose_name='شهر')
    location    = PlainLocationField(based_fields=['city'], zoom=8 ,suffix=['city'], verbose_name='موقعیت مکانی')
    date_start  = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ شروع پروژه')
    date_end    = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ پایان پروژه')
    view_count  = models.IntegerField(default=0,editable=False,  verbose_name='تعداد بازدید')
    #
    mojavez     = models.FileField(upload_to='files/images/project/mojavez', verbose_name='مجوزهای پروژه', default="")
    mostanadat  = models.FileField(upload_to='files/images/project/mostanadat', verbose_name='مستندات پروژه', default="")
    file_ha     = models.FileField(upload_to='files/images/project', verbose_name='فایلهای پروژه', default="")

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه"
    def __str__(self):
        return self.title



class subproject(models.Model):
    title       = models.CharField(max_length=202, null=False , blank=False , verbose_name='عنوان')
    photo       = models.ImageField(upload_to='files/images/project/sub',verbose_name='تصویر زیرپروژه', default="")
    project_id  = models.ForeignKey(project, blank=False, null=False, on_delete=models.CASCADE, verbose_name="پروژه مربوطه")
    type        = models.ForeignKey(map_object_types, blank=False,null=False, on_delete=models.CASCADE, verbose_name='نوع پروژه')
    pishrafte_kol = models.IntegerField(validators=[validate_darsad],verbose_name='پیشرفت کل')
    date_start  = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ شروع')
    date_end    = models.DateTimeField(default=datetime.now(), verbose_name='تاریخ پایان')
    team        = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مدیر پروژه')
    view_count  = models.IntegerField(default=0,editable=False,  verbose_name='تعداد بازدید' )
    #
    naghshe     = models.FileField(upload_to='files/images/subproject/naghshe', blank=True,null=True, verbose_name='نقشه اجرا', default="")
    mojavez     = models.FileField(upload_to='files/images/subproject/mojavez', blank=True,null=True, verbose_name='مجوزهای پروژه', default="")
    mostanadat  = models.FileField(upload_to='files/images/subproject/mostanadat', blank=True,null=True, verbose_name='مستندات پروژه', default="")
    file_ha     = models.FileField(upload_to='files/images/subproject', blank=True,null=True, verbose_name='فایلهای پروژه', default="")
    #
    marhale1     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 1')
    marhale2     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 2')
    marhale3     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 3')
    marhale4     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 4')
    marhale5     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 5')
    marhale6     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 6')
    marhale7     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 7')
    marhale8     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 8')
    marhale9     = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 9')
    marhale10    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 10')
    marhale11    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 11')
    marhale12    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 12')
    marhale13    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 13')
    marhale14    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 14')
    marhale15    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 15')
    marhale16    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 16')
    marhale17    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 17')
    marhale18    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 18')
    marhale19    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 19')
    marhale20    = models.CharField(max_length=202, blank=True,null=True, default="", verbose_name='مرحله 20')

    class Meta:
        verbose_name = "زیرپروژه ها"
        verbose_name_plural = "زیرپروژه"

    def __str__(self):
        return self.title

