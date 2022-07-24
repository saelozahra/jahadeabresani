from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "اطلاعات شخصی",
            {
                "fields":
                    (
                        "city",
                        "address",
                        "phone",
                        "melli",
                        "is_project_admin",
                    )
            },
        )
    )
    add_form = CustomUserCreationForm


admin.site.register(CustomUser, CustomUserAdmin)
