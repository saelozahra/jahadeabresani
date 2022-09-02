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



class Chat(models.Model):
    User1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE, verbose_name='کاربر 1')
    User2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE, verbose_name='کاربر 2')
    Zaman = models.CharField(editable=False, default=datetime.now(), max_length=202, verbose_name='زمان آخرین پیام')
    Lead = models.TextField(editable=False, verbose_name='خلاصه آخرین پیام')

    class Meta:
        verbose_name = "چت"
        verbose_name_plural = "چت"

    def __str__(self):
        return "مکالمه " + self.User1.get_short_name() + " و " + self.User2.get_short_name()


class ChatMessage(models.Model):
    RelatedChat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='مربوط به چت')
    Sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده', blank=True, null=True)
    Text = models.TextField(default="", verbose_name='متن پیام')
    Tarikh = models.CharField(editable=False, blank=True ,null=True ,max_length=202, verbose_name='زمان')
    Attachments = models.ImageField(upload_to='files/images/ticket-attachs', verbose_name='پیوست', default="", blank=True)
    Readed = models.BooleanField(editable=False, verbose_name='دیده شده', default=False)
    Visible = models.BooleanField(editable=False, verbose_name='نمایان', default=True)

    class Meta:
        verbose_name = "پیام‌ها"
        verbose_name_plural = "پیام‌ها"

    def save(self, *args, **kwargs):
        if self.Tarikh is None or self.Tarikh == "":
            print("Tarikh none hast")
            self.Tarikh = datetime.now()
        self.RelatedChat.Lead = self.Text[:202]
        self.RelatedChat.save()
        self.RelatedChat.Zaman = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.Text[:133]+"..."

    def jdate_tarikh(self):
        return self.Tarikh

