from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    city = models.CharField(default="",null=True, blank=True, max_length=24, verbose_name="شهر")
    address = models.CharField(default="",null=True, blank=True, max_length=202, verbose_name="نشانی منزل")
    phone = models.CharField(default="", null=False, blank=False, max_length=11, verbose_name="شماره تماس")
    melli = models.CharField(default="", null=False, blank=False, max_length=10, verbose_name="کد ملی")
    is_project_admin = models.BooleanField(default=False, verbose_name="آیا مدیر پروژه هست؟")

    class Meta:
        verbose_name = "کاربران"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.first_name + " " + self.last_name
