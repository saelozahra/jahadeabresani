from django.db.models import Q
import accounts.models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_jalali.db.models import jDateTimeField
from django.db import models
from django_jalali.db import models as jmodels
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User, Group


def mohasebe_darsad(self, kol, jozea):
    print(kol)
    print(jozea)
    if kol == 0:
        print("khali")
        return 0
    elif kol == jozea:
        print("tamam")
        return 100
    else:
        print("herelley")
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


class MaraheleEjra(models.Model):
    marhale = models.CharField(max_length=110, verbose_name='نام مرحله', null=False, blank=False)
    vahed = models.CharField(max_length=110, verbose_name='واحد', null=True, blank=True)

    class Meta:
        verbose_name = "مراحل اجرا"
        verbose_name_plural = "مراحل اجرا"

    def __str__(self):
        return self.marhale


class Project(models.Model):
    objects = jmodels.jManager()
    title = models.CharField(max_length=202, verbose_name='عنوان')
    slug = models.SlugField(null=True, unique=True, verbose_name='نشانی لینک')
    photo = models.ImageField(upload_to='files/images/project', verbose_name='تصویر پروژه', default="")
    city = models.CharField(max_length=202, verbose_name='شهر')
    location = PlainLocationField(based_fields=['city'], zoom=4, suffix=['city'], verbose_name='موقعیت مکانی')
    miangin_pishraft = models.IntegerField(default=0, editable=False, verbose_name='میانگین پیشرفت کل')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    #
    note = models.TextField(default="", verbose_name='یادداشت', blank=True, null=True)

    #
    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def thumbnail_preview(self):
        if self.photo:
            return mark_safe(
                '<img src="{}" style="object-fit:contain; height:auto; max-height:110px; " width="110" />'.format(
                    self.photo.url))
        return ""


class SubProject(models.Model):
    title = models.CharField(max_length=202, null=False, blank=False, verbose_name='عنوان')
    photo = models.ImageField(upload_to='files/images/project/sub', verbose_name='تصویر زیرپروژه', default="")
    project_id = models.ForeignKey(Project, blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="پروژه مربوطه")
    type = models.ForeignKey(MapObjectTypes, blank=False, null=False, on_delete=models.CASCADE,
                             verbose_name='نوع پروژه')
    pishrafte_kol = models.IntegerField(validators=[validate_darsad], verbose_name='پیشرفت کل')
    date_start = jmodels.jDateField(verbose_name='تاریخ شروع')
    date_end = jmodels.jDateField(verbose_name='تاریخ پایان')
    team = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, verbose_name='مدیر پروژه')
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
    marhale21 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 21')
    marhale21full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 21')
    marhale21accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 21')
    marhale22 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 22')
    marhale22full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 22')
    marhale22accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 22')
    marhale23 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 23')
    marhale23full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 23')
    marhale23accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 23')
    marhale24 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 24')
    marhale24full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 24')
    marhale24accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 24')
    marhale25 = models.CharField(max_length=202, blank=True, null=True, default="", verbose_name='متن مرحله 25')
    marhale25full = models.IntegerField(default="0", verbose_name='واحد کل | مرحله 25')
    marhale25accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده | مرحله 25')

    def save(self, *args, **kwargs):
        real_miangin_all = 0
        real_miangin_count = 0

        if self.marhale1full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale1full.__str__(), self.marhale1accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale2full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale2full.__str__(), self.marhale2accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale3full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale3full.__str__(), self.marhale3accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale4full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale4full.__str__(), self.marhale4accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale5full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale5full.__str__(), self.marhale5accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale6full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale6full.__str__(), self.marhale6accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale7full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale7full.__str__(), self.marhale7accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale8full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale8full.__str__(), self.marhale8accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale9full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale9full.__str__(), self.marhale9accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale10full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale10full.__str__(), self.marhale10accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale11full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale11full.__str__(), self.marhale11accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale12full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale12full.__str__(), self.marhale12accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale13full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale13full.__str__(), self.marhale13accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale14full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale14full.__str__(), self.marhale14accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale15full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale15full.__str__(), self.marhale15accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale16full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale16full.__str__(), self.marhale16accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale17full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale17full.__str__(), self.marhale17accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale18full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale18full.__str__(), self.marhale18accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale19full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale19full.__str__(), self.marhale19accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale20full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale20full.__str__(), self.marhale20accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale21full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale21full.__str__(), self.marhale21accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale22full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale22full.__str__(), self.marhale22accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale23full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale23full.__str__(), self.marhale23accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale24full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale24full.__str__(), self.marhale24accomplished.__str__())
            real_miangin_count = real_miangin_count + 1
        elif self.marhale25full.__str__():
            real_miangin_all = mohasebe_darsad(self, self.marhale25full.__str__(), self.marhale25accomplished.__str__())
            real_miangin_count = real_miangin_count + 1

        if real_miangin_all:
            self.pishrafte_kol = real_miangin_all / real_miangin_count
        else:
            self.pishrafte_kol = 0

        subs = SubProject.objects.filter(Q(project_id__slug__contains=self.project_id.slug))
        miangin_pishrafte_project = 0
        miangin_pishrafte_project_count = 0

        for spd_temp in subs:
            miangin_pishrafte_project=miangin_pishrafte_project+spd_temp.pishrafte_kol
            miangin_pishrafte_project_count=miangin_pishrafte_project_count+1

        if miangin_pishrafte_project == 0:
            self.project_id.miangin_pishraft = 0
        else:
            self.project_id.miangin_pishraft = miangin_pishrafte_project/miangin_pishrafte_project_count

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "زیرپروژه ها"
        verbose_name_plural = "زیرپروژه"

    def __str__(self):
        return self.title
