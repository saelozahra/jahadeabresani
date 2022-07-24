import accounts.models
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User, Group


# Create your models here.

class Department(models.Model):
    Title       = models.CharField(max_length=202, verbose_name='نام دپارتمان')
    UserGroup   = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='گروه کاربری')
    Desc        = models.TextField(default="" ,verbose_name='یادداشت' )

    class Meta:
        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان"

    def __str__(self):
        return self.Title


class Ticket(models.Model):
    Title   = models.CharField(max_length=202, verbose_name='موضوع')
    User    = models.ForeignKey(accounts.models.CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    Zaman  = models.CharField(max_length=202, verbose_name='زمان آخرین تغییر')
    RelatedDepartment = models.ForeignKey(Department, blank=False, null=False, on_delete=models.CASCADE, verbose_name='دپارتمان')
    Attachments = models.ImageField(upload_to='files/images/ticket-attachs', verbose_name='پیوست', default="")
    Note    = models.TextField(default="", verbose_name='یادداشت مدیریت' )

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت"

    def __str__(self):
        return self.Title + " از " + self.User.get_short_name()


class TicketMessage(models.Model):
    objects = jmodels.jManager()
    RelatedTicket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='مربوط به تیکت')
    Text    = models.TextField(default="" ,verbose_name='متن تیکت' )
    Tarikh  = jmodels.jDateTimeField(verbose_name='تاریخ')
    Attachments = models.ImageField(upload_to='files/images/ticket-attachs', verbose_name='پیوست', default="")

    class Meta:
        verbose_name = "پیام ها"
        verbose_name_plural = "پیام ها"

    def __str__(self):
        return self.Title

    def jdate_tarikh(self):
        return self.Tarikh
