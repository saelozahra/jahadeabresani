import main.models
from main.models import *
# Create your models here.


class Events(models.Model):
    RelatedProject = models.ForeignKey(Project, blank=False, null=False, on_delete=models.CASCADE,
                                       verbose_name="پروژه مربوطه")
    OwnerUser = models.ForeignKey(accounts.models.CustomUser, null=False, on_delete=models.CASCADE,
                                  verbose_name="کاربر مربوطه")
    EventType = models.CharField(max_length=313, verbose_name='نوع رویداد')
    day = jmodels.jDateField(verbose_name='روز', editable=True, auto_now_add=True)
    do_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='زمان دقیق')
    description = models.TextField(default="", verbose_name='توضیحات', blank=True)
    # status = models.IntegerField(default=0, editable=False, verbose_name='وضعیت')

    def save(self, *args, **kwargs):
        # if self.OwnerUser is None:
        #     self.OwnerUser = self.
        main.models.Project.objects.filter(Q(id=self.RelatedProject.id)).update(last_update=self.do_time)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "رویدادها"
        verbose_name_plural = "رویدادهای پروژه"

    def __str__(self):
        return "تغییر در پروژه " + self.RelatedProject.__str__() +\
               " توسط " + self.OwnerUser.__str__() + " در " + self.day.__str__()
