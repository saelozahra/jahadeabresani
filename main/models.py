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
import sys
from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from inline_ordering.models import Orderable

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

    class Meta:
        verbose_name = "نوع پروژه"
        verbose_name_plural = "نوع پروژه"

    def __str__(self):
        return self.title

    def get_marahels(self):
        return self.marhalel_ejra_s.all().count()


class MaraheleEjra(Orderable):
    VahedChoices = (
        (0, 'متر'),
        (1, 'کیلومتر'),
        (2, 'کیلو'),
        (3, 'متر مربع'),
        (4, 'پروژه'),
        (5, 'x'),
    )
    Project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="مراحل اجرای پروژه")
    marhale = models.CharField(max_length=110, verbose_name='نام مرحله', null=False, blank=False)
    vahed = models.PositiveSmallIntegerField(choices=VahedChoices,default=0, verbose_name='واحد')
    description = models.TextField(blank=True, null=True, default="", verbose_name='توضیحات این مرحله')
    marhale_full = models.IntegerField(default="0", verbose_name='واحد کل')
    marhale_accomplished = models.IntegerField(default="0", verbose_name='واحد انجام شده')

    @property
    def marhale_percent(self):
        return calculate_percent(self.marhale_full, self.marhale_accomplished)


    @property
    def vahed_name(self):
        name_val = dict(self.VahedChoices).get(self.vahed)
        return name_val


    class Meta(Orderable.Meta):
        verbose_name = "مرحله اجرا"
        verbose_name_plural = "مرحله اجرا"

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
    thumbnails = models.ImageField(upload_to='files/images/project/sub/thumbnail', editable=False, blank=True, verbose_name='تصویرک')
    RelatedCity = models.ForeignKey(CityProject, blank=False, null=True, on_delete=models.CASCADE, verbose_name="شهر مربوطه")
    type = models.ForeignKey(MapObjectTypes, blank=False, null=False, on_delete=models.CASCADE, verbose_name='نوع پروژه')
    money = models.IntegerField(default=0, verbose_name='بودجه پروژه', help_text="بودجه به تومان")
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

    def save(self, *args, **kwargs):

        output_size = (313, 313)
        output_thumb = BytesIO()

        img = Image.open(self.photo)
        img_name = self.photo.name.split('.')[0]

        if img.height > 313 or img.width > 313:
            img.thumbnail(output_size)
            img.save(output_thumb,format='JPEG', quality=90)

        self.thumbnails = InMemoryUploadedFile(output_thumb, 'ImageField', f"{img_name}_thumb.jpg", 'image/jpeg', sys.getsizeof(output_thumb), None)

        real_miangin_all = 0
        real_miangin_count = 0
        for m in MaraheleEjra.objects.filter(Project_id=self.id).all():
            if m.marhale_accomplished.numerator > 0:
                real_miangin_all = real_miangin_all + calculate_percent(m.marhale_full.numerator, m.marhale_accomplished.numerator)
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
                    self.thumbnails.url))
        return ""


@receiver(models.signals.post_save, sender=Project)
def proj_save(sender, instance, created, **kwargs):
    update_avg_city(instance.RelatedCity)
    print('post save callback')
