from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class CityProject(models.Model):
    city = models.CharField(max_length=202, verbose_name='نام شهر')
    slug = models.SlugField(null=True, unique=True, verbose_name='نام انگلیسی',
                            help_text="نام انگلیسی شهر را وارد کنید")
    miangin_pishraft = models.IntegerField(default=0, editable=False, verbose_name='میانگین پیشرفت کل')
    view_count = models.IntegerField(default=0, editable=False, verbose_name='تعداد بازدید')
    note = models.TextField(default="", verbose_name='یادداشت', blank=True, null=True)

    class Meta:
        verbose_name = "شهرها"
        verbose_name_plural = "شهرها"

    def __str__(self):
        return self.city

    def get_absolute_url(self):
        return reverse("project", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.city)
        return super().save(*args, **kwargs)

